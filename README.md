# IdeaForge AI — Multi-Agent Innovation Pipeline

> **From Idea to IP-Ready Innovation** — an end-to-end agentic system that transforms unstructured innovation briefs into structured, novelty-validated, IP-ready concept reports.

---

## Architecture

```
User Brief
    ↓
┌─────────────────────────────────────────────────────────┐
│  FastAPI  (WebSocket streaming + REST)                   │
└────────────────────────┬────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  LangGraph Pipeline                                      │
│                                                          │
│  [Supervisor] → [Ideation] → [Prior Art] → [Synthesis]  │
│                                                          │
│  • Supervisor   — ReAct planner, strategic framing       │
│  • Ideation     — KG-augmented concept generator         │
│  • Prior Art    — arXiv + Semantic Scholar search        │
│  • Synthesis    — IP-readiness report + novelty score    │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  Knowledge Layer                                         │
│  NetworkX knowledge graph  (tech × domain × patterns)   │
└─────────────────────────────────────────────────────────┘
```

### Key Components

| Layer | Technology |
|---|---|
| Orchestration | **LangGraph** (StateGraph, ReAct-style nodes) |
| LLM backend | **OpenAI GPT-4o-mini** (or gpt-4o / gpt-4-turbo) |
| Knowledge graph | **NetworkX** — tech × domain × innovation-pattern graph |
| Academic search | **arXiv API** + **Semantic Scholar open API** |
| Backend | **FastAPI** with async WebSocket streaming |
| Frontend | Vanilla HTML/CSS/JS — dark theme, real-time pipeline UI |

---

## Quick Start

### 1 — Clone and set up Python environment

```bash
cd backend
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 2 — Configure environment

```bash
# From the repo root
copy .env.example .env     # Windows
cp   .env.example .env     # macOS / Linux
```

Open `.env` and set your `OPENAI_API_KEY`.  
**If you skip this step the system runs in DEMO mode** — all outputs are realistic mock data; no API key is required.

### 3 — Start the server

```powershell
# PowerShell (Windows) — from the repo root
Push-Location backend
.\.venv\Scripts\uvicorn.exe main:app --host 0.0.0.0 --port 8000 --reload
```

```bash
# macOS / Linux — from the repo root
cd backend
.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4 — Open the UI

Navigate to **http://localhost:8000** in your browser.

---

## How It Works

### 1. Supervisor Agent
Analyses the innovation brief (domain + problem space + intent) and creates a structured strategic plan:
- Focus areas, innovation angles, validation priorities
- Tailored search queries for prior art

### 2. Ideation Agent
Queries the **NetworkX knowledge graph** to discover relevant technology→domain connections, then asks the LLM to generate **3 distinct, technically grounded innovation concepts**, each with:
- Title, description, technical approach
- Use cases, implementation pathway
- Strategic positioning, novelty indicators

### 3. Prior Art Search Agent
For each concept, searches **arXiv** and **Semantic Scholar** in parallel (real API calls — no auth needed).  
Uses LLM to score relevance and surface key differences from prior art.

### 4. Synthesis Agent
Produces the final **IP-readiness report**:
- Novelty assessment (score 0–100, High/Medium/Low rating)
- Executive summary (4 paragraphs)
- Actionable next steps for patent filing

All intermediate results stream live to the browser via **WebSocket**.

---

## Project Structure

```
code_agent_1_ideation_to_IP/
├── backend/
│   ├── main.py                  # FastAPI app + WebSocket + static serving
│   ├── config.py                # Env vars + demo-mode flag
│   ├── events.py                # Async channel manager for WS streaming
│   ├── requirements.txt
│   ├── agents/
│   │   ├── supervisor.py        # Supervisor / orchestrator node
│   │   ├── ideation.py          # Ideation agent node
│   │   ├── prior_art.py         # Prior art search + scoring node
│   │   └── synthesis.py         # IP report synthesis node
│   ├── graph/
│   │   └── workflow.py          # LangGraph StateGraph definition
│   ├── knowledge/
│   │   ├── domain_data.py       # Pre-loaded nodes & edges
│   │   └── knowledge_graph.py   # NetworkX KG + query helpers
│   ├── models/
│   │   └── schemas.py           # Pydantic models
│   └── tools/
│       ├── arxiv_search.py      # arXiv async search
│       └── semantic_scholar.py  # Semantic Scholar async search
├── frontend/
│   ├── index.html               # Single-page app
│   ├── styles.css               # Dark-theme professional UI
│   └── app.js                   # WS client + real-time rendering
└── .env.example
```

---

## Live vs Demo Mode

| | Live Mode | Demo Mode |
|---|---|---|
| Trigger | `OPENAI_API_KEY` set in `.env` | Key missing / placeholder |
| LLM calls | Real OpenAI API | Realistic mock responses |
| Prior art search | Real arXiv + S2 API calls | Pre-loaded mock papers |
| Cost | ~$0.01–0.05 per run (gpt-4o-mini) | Free |
| UI indicator | — | `DEMO MODE` badge |

---

## Extending the System

- **Add a new agent node**: create `backend/agents/my_agent.py`, add it to `graph/workflow.py`.
- **Swap the LLM**: change `OPENAI_MODEL` in `.env` or replace the `ChatOpenAI` calls with any LangChain-compatible LLM.
- **Add patent database search**: extend `tools/` with a Google Patents or USPTO API client, then call it from `prior_art.py`.
- **Persist results**: add a SQLite / PostgreSQL integration to save session outputs.

---

## Legal & Authorship

This README, the codebase, and all project materials in this repository are the sole work of the author.

This system is documented and maintained to support a filed patent application. All rights are reserved by the author, and the project should be treated as proprietary intellectual property related to that filing.
