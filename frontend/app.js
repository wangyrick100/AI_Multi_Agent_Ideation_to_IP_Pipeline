/**
 * IdeaForge AI — Frontend Application
 *
 * Manages WebSocket connection, real-time pipeline updates,
 * and result rendering.
 */

const API_BASE = window.location.origin;

// ─────────────────────────────────────────────────────────────────────────────
// State
// ─────────────────────────────────────────────────────────────────────────────
let ws = null;
let sessionId = null;
let finalOutput = null;

const AGENT_ORDER = ['supervisor', 'ideation', 'prior_art', 'synthesis'];
const AGENT_PROGRESS = { supervisor: 20, ideation: 50, prior_art: 80, synthesis: 100 };

// ─────────────────────────────────────────────────────────────────────────────
// DOM helpers
// ─────────────────────────────────────────────────────────────────────────────
const $ = id => document.getElementById(id);
const show = id => $( id)?.classList.remove('hidden');
const hide = id => $( id)?.classList.add('hidden');
const text = (id, v) => { if ($(id)) $(id).textContent = v; };

function escHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// ─────────────────────────────────────────────────────────────────────────────
// Toast notifications
// ─────────────────────────────────────────────────────────────────────────────
function showToast(msg, type = 'info', duration = 4000) {
  const el = document.createElement('div');
  el.className = `toast ${type}`;
  el.textContent = msg;
  $('toast-container').appendChild(el);
  setTimeout(() => el.remove(), duration);
}

// ─────────────────────────────────────────────────────────────────────────────
// Pipeline node states
// ─────────────────────────────────────────────────────────────────────────────
function setNodeState(agent, state, statusText) {
  // normalise agent id for DOM (prior_art → prior-art for node id)
  const domId = `node-${agent.replace('_', '-')}`;
  const nodeEl = document.getElementById(domId);
  if (!nodeEl) return;

  nodeEl.classList.remove('state-running', 'state-complete', 'state-error');
  if (state) nodeEl.classList.add(`state-${state}`);

  const badge = $(`badge-${agent}`);
  if (badge) badge.textContent = statusText || state || 'waiting';
}

function setProgress(pct, label) {
  const bar = $('progress-bar');
  if (bar) bar.style.width = `${pct}%`;
  if (label) text('progress-label', label);
}

// ─────────────────────────────────────────────────────────────────────────────
// Status log
// ─────────────────────────────────────────────────────────────────────────────
function appendLog(msg, type = '') {
  const container = $('log-entries');
  if (!container) return;

  const entry = document.createElement('div');
  entry.className = `log-entry ${type}`;
  entry.textContent = `[${new Date().toLocaleTimeString()}] ${msg}`;
  container.appendChild(entry);
  container.scrollTop = container.scrollHeight;
}

// ─────────────────────────────────────────────────────────────────────────────
// WebSocket
// ─────────────────────────────────────────────────────────────────────────────
function openWebSocket(sid) {
  const proto = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const url = `${proto}//${window.location.host}/ws/${sid}`;
  ws = new WebSocket(url);

  ws.onopen  = () => appendLog('WebSocket connected.', 'active');
  ws.onerror = () => { showToast('WebSocket error — check backend.', 'error'); appendLog('WS error', 'error'); };
  ws.onclose = () => appendLog('WebSocket closed.');

  ws.onmessage = ({ data }) => {
    let event;
    try { event = JSON.parse(data); } catch { return; }
    if (event.type === 'ping') return;
    handlePipelineEvent(event);
  };
}

// ─────────────────────────────────────────────────────────────────────────────
// Event handler
// ─────────────────────────────────────────────────────────────────────────────
function handlePipelineEvent(event) {
  const { type, agent, message, data } = event;
  appendLog(`[${agent}] ${message}`, type === 'error' ? 'error' : type === 'agent_complete' ? 'success' : 'active');

  switch (type) {
    case 'agent_start':
      setNodeState(agent, 'running', 'Running…');
      setProgress(AGENT_PROGRESS[agent] - 15, message);
      break;

    case 'agent_progress':
      setProgress(AGENT_PROGRESS[agent] - 8, message);
      break;

    case 'agent_complete':
      setNodeState(agent, 'complete', 'Done');
      setProgress(AGENT_PROGRESS[agent], message);

      // Partial renders as agents finish
      if (agent === 'ideation' && data?.concepts) {
        renderConcepts(data.concepts);
      }
      if (agent === 'prior_art' && data?.prior_art_results) {
        renderPriorArt(data.prior_art_results);
      }
      break;

    case 'pipeline_complete':
      finalOutput = data;
      renderFullReport(data);
      resetFormState(false);
      show('results-area');
      showToast(
        `Pipeline complete! IP Score: ${data.ip_readiness_score?.toFixed(0)}/100`,
        'success', 6000
      );
      setProgress(100, `Complete — IP Readiness: ${data.ip_readiness_score?.toFixed(0)}/100`);
      break;

    case 'error':
      setNodeState(agent, 'error', 'Error');
      showToast(`Error: ${message}`, 'error');
      appendLog(message, 'error');
      resetFormState(false);
      break;
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// Form submission
// ─────────────────────────────────────────────────────────────────────────────
$('innovation-form').addEventListener('submit', async e => {
  e.preventDefault();
  await runPipeline();
});

async function runPipeline() {
  const domain        = $('domain').value.trim();
  const problemSpace  = $('problem-space').value.trim();
  const userIntent    = $('user-intent').value.trim();
  const depth         = $('depth').value;

  if (!domain || !problemSpace || !userIntent) {
    showToast('Please fill in all required fields.', 'error');
    return;
  }

  // Reset UI
  resetPipelineUI();
  resetFormState(true);
  show('status-log');
  show('results-area');

  // New session
  sessionId = await fetchSessionId();

  // Open WebSocket before triggering the pipeline
  openWebSocket(sessionId);

  // Give WS a moment to connect
  await sleep(200);

  try {
    const resp = await fetch(`${API_BASE}/api/innovate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id:    sessionId,
        domain,
        problem_space: problemSpace,
        user_intent:   userIntent,
        depth,
      }),
    });
    const result = await resp.json();

    if (result.demo_mode) {
      show('demo-badge');
      showToast('Running in DEMO mode — set OPENAI_API_KEY for live results.', 'info', 7000);
    }
  } catch (err) {
    showToast(`Failed to start pipeline: ${err.message}`, 'error');
    resetFormState(false);
  }
}

async function fetchSessionId() {
  try {
    const r = await fetch(`${API_BASE}/api/session`);
    const d = await r.json();
    return d.session_id;
  } catch {
    return crypto.randomUUID();
  }
}

function resetFormState(loading) {
  const btn     = $('submit-btn');
  const btnText = $('btn-text');
  const spinner = $('btn-spinner');
  btn.disabled = loading;
  if (loading) { btnText.textContent = 'Running…'; show('btn-spinner'); }
  else         { btnText.textContent = 'Run Innovation Pipeline'; hide('btn-spinner'); }
}

function resetPipelineUI() {
  AGENT_ORDER.forEach(a => setNodeState(a, '', 'Waiting'));
  setProgress(0, 'Pipeline starting…');
  hide('overview-content');   show('overview-placeholder');
  hide('concepts-content');   show('concepts-placeholder');
  hide('prior-art-content');  show('prior-art-placeholder');
  hide('ip-report-content');  show('ip-report-placeholder');
  $('log-entries').innerHTML = '';
  hide('demo-badge');
  finalOutput = null;

  // Clear badge counts
  hide('tab-badge-concepts');
  hide('tab-badge-prior-art');
}

// ─────────────────────────────────────────────────────────────────────────────
// Renderers
// ─────────────────────────────────────────────────────────────────────────────
function renderConcepts(concepts) {
  const grid = $('concepts-content');
  grid.innerHTML = concepts.map((c, i) => `
    <div class="concept-card">
      <div class="concept-header">
        <div class="concept-number">${i + 1}</div>
        <div>
          <div class="concept-title">${escHtml(c.title)}</div>
          <div class="concept-description">${escHtml(c.description)}</div>
        </div>
      </div>

      <div class="concept-section">
        <div class="concept-section-label">Technical Approach</div>
        <div class="concept-section-body">${escHtml(c.technical_approach)}</div>
      </div>

      <div class="concept-section">
        <div class="concept-section-label">Use Cases</div>
        <div class="tag-list">${(c.use_cases || []).map(u => `<span class="tag">${escHtml(u)}</span>`).join('')}</div>
      </div>

      <div class="concept-section">
        <div class="concept-section-label">Strategic Positioning</div>
        <div class="concept-section-body">${escHtml(c.strategic_positioning)}</div>
      </div>

      <div class="concept-section">
        <div class="concept-section-label">Novelty Indicators</div>
        <div class="tag-list">${(c.novelty_indicators || []).map(n => `<span class="tag novelty">${escHtml(n)}</span>`).join('')}</div>
      </div>
    </div>
  `).join('');

  hide('concepts-placeholder');
  show('concepts-content');
  const badge = $('tab-badge-concepts');
  if (badge) { badge.textContent = concepts.length; show('tab-badge-concepts'); }
}

function renderPriorArt(priorArtResults) {
  const container = $('prior-art-content');
  let totalPapers = 0;

  container.innerHTML = priorArtResults.map(block => {
    const papers = block.results || [];
    totalPapers += papers.length;
    return `
      <div class="prior-art-concept-block">
        <div class="prior-art-concept-title">Concept ${block.concept_index + 1}: ${escHtml(block.concept_title)}</div>
        ${papers.length === 0
          ? '<p class="placeholder-msg" style="padding:16px">No prior art found.</p>'
          : papers.map(p => renderPaperCard(p)).join('')
        }
      </div>
    `;
  }).join('');

  hide('prior-art-placeholder');
  show('prior-art-content');
  const badge = $('tab-badge-prior-art');
  if (badge) { badge.textContent = totalPapers; show('tab-badge-prior-art'); }
}

function renderPaperCard(p) {
  const score = p.relevance_score || 0;
  const pct   = Math.round(score * 100);
  const cls   = score >= 0.65 ? 'relevance-high' : score >= 0.4 ? 'relevance-medium' : 'relevance-low';
  const srcCls = `source-${p.source}`;
  const titleHtml = p.url
    ? `<a href="${escHtml(p.url)}" target="_blank" rel="noopener">${escHtml(p.title)}</a>`
    : escHtml(p.title);

  return `
    <div class="paper-card">
      <div class="paper-top">
        <div class="paper-title">
          ${titleHtml}
          <span class="source-tag ${srcCls}">${escHtml(p.source.replace('_', ' '))}</span>
        </div>
        <div class="paper-relevance ${cls}">${pct}% match</div>
      </div>
      <div class="paper-meta">${escHtml((p.authors || []).join(', '))} · ${p.year || '—'}</div>
      ${p.summary ? `<div class="concept-section-body" style="font-size:.8rem;color:var(--text-sub)">${escHtml(p.summary.slice(0,280))}…</div>` : ''}
      ${p.key_differences ? `<div class="paper-diff">${escHtml(p.key_differences)}</div>` : ''}
    </div>
  `;
}

function renderFullReport(data) {
  if (!data) return;

  // ── Overview ──────────────────────────────────────────────────────────────
  const ip = data.ip_readiness_score ?? 0;
  const novelty = data.novelty_assessment ?? {};

  $('metric-ip-score').textContent = `${ip.toFixed(0)}/100`;
  $('metric-novelty').textContent  = novelty.rating ?? '—';
  const nColor = novelty.rating === 'High' ? 'var(--success)' : novelty.rating === 'Medium' ? 'var(--warning)' : 'var(--danger)';
  $('metric-novelty').style.color = nColor;
  $('metric-concepts').textContent = (data.innovation_concepts ?? []).length;
  $('metric-papers').textContent   = (data.prior_art_results ?? []).reduce((s, b) => s + (b.results ?? []).length, 0);

  const summaryEl = $('executive-summary');
  if (summaryEl) summaryEl.textContent = data.executive_summary ?? '';

  const nextStepsList = $('next-steps-list');
  if (nextStepsList) {
    nextStepsList.innerHTML = (data.next_steps ?? []).map(s => `<li>${escHtml(s)}</li>`).join('');
  }

  hide('overview-placeholder');
  show('overview-content');

  // ── IP Report ─────────────────────────────────────────────────────────────
  const difList = $('differentiator-list');
  if (difList) {
    difList.innerHTML = (novelty.key_differentiators ?? []).map(d => `<li>${escHtml(d)}</li>`).join('');
  }
  const riskList = $('risk-list');
  if (riskList) {
    riskList.innerHTML = (novelty.risk_areas ?? []).map(r => `<li>${escHtml(r)}</li>`).join('');
  }

  const noveltyDetails = $('novelty-details');
  if (noveltyDetails) {
    noveltyDetails.innerHTML = `
      <div style="display:flex;align-items:center;gap:16px;margin-bottom:8px">
        <div style="font-size:2.5rem;font-weight:800;color:${nColor}">${(novelty.overall_score ?? 0).toFixed(1)}</div>
        <div>
          <div style="font-size:1rem;font-weight:700;color:${nColor}">${escHtml(novelty.rating ?? '—')} Novelty</div>
          <div style="font-size:.75rem;color:var(--text-sub)">Novelty score out of 100</div>
        </div>
      </div>
    `;
  }

  const rec = $('recommendation-text');
  if (rec) rec.textContent = novelty.recommendation ?? '';

  hide('ip-report-placeholder');
  show('ip-report-content');

  // Ensure concepts and prior art are rendered too
  if (data.innovation_concepts?.length) renderConcepts(data.innovation_concepts);
  if (data.prior_art_results?.length)   renderPriorArt(data.prior_art_results);

  // Switch to overview tab
  activateTab('overview');
}

// ─────────────────────────────────────────────────────────────────────────────
// Tabs
// ─────────────────────────────────────────────────────────────────────────────
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => activateTab(btn.dataset.tab));
});

function activateTab(tabName) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.toggle('active', b.dataset.tab === tabName));
  document.querySelectorAll('.tab-content').forEach(c => {
    c.classList.toggle('active', c.id === `tab-${tabName}`);
  });
}

// ─────────────────────────────────────────────────────────────────────────────
// Utility
// ─────────────────────────────────────────────────────────────────────────────
const sleep = ms => new Promise(r => setTimeout(r, ms));

// ─────────────────────────────────────────────────────────────────────────────
// Health check on load
// ─────────────────────────────────────────────────────────────────────────────
(async () => {
  try {
    const r = await fetch(`${API_BASE}/api/health`);
    const d = await r.json();
    if (d.demo_mode) {
      show('demo-badge');
    }
  } catch {
    showToast('Cannot reach backend — is the server running?', 'error', 8000);
  }
})();
