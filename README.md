# IdeaForge AI

> Proprietary multi-agent innovation-to-IP pipeline authored and owned by Yang (Rick) Wang, Ph.D.

## Proprietary Notice

This repository contains proprietary source code, architecture, prompts, workflows, documentation, and invention-support materials that are the property of **Yang (Rick) Wang, Ph.D.**

Certain systems, methods, workflows, and technical embodiments reflected in this repository are associated with one or more **already-filed patent applications** owned or controlled by **Yang (Rick) Wang, Ph.D.** Access to this repository, publication of this README, or review of the code does **not** grant any license, assignment, waiver, release, or other permission to copy, reproduce, distribute, commercialize, reverse engineer, train on, benchmark against for derivative commercialization, or otherwise exploit the materials herein except with prior written authorization.

Except for third-party libraries, frameworks, APIs, and dependencies that remain subject to their own licenses and terms, this solution and its original implementation are private property and all rights are reserved.

## Author and Ownership

- Author / owner: **Yang (Rick) Wang, Ph.D.**
- Repository status: **Proprietary**
- Patent status: **Already filed / patent-pending subject matter is reflected in this solution**
- Intended use of this README: technical system description, engineering reference, invention-support record, and patent-discussion support document

## Executive Summary

IdeaForge AI is an end-to-end agentic system that transforms an unstructured innovation brief into a structured, reviewable, and IP-oriented output package. The platform orchestrates four cooperating agents:

1. A **Supervisor** agent that frames the innovation problem and defines search strategy.
2. An **Ideation** agent that combines LLM reasoning with a domain knowledge graph to generate technically differentiated concepts.
3. A **Prior Art** agent that performs academic prior-art screening across arXiv and Semantic Scholar and scores conceptual overlap.
4. A **Synthesis** agent that compiles a novelty-oriented report, IP-readiness score, and recommended next actions.

The system is designed to reduce the gap between raw brainstorming and invention-grade technical documentation. It does not merely generate ideas; it structures them into a workflow that is more suitable for invention disclosure, technical diligence, claim-scope discussion, and follow-on patent counsel review.

## Why This System Matters

In early-stage invention work, teams often struggle with four recurring problems:

- valuable ideas remain trapped in informal notes or conversations
- novelty analysis is inconsistent and difficult to repeat
- prior-art review is too shallow or too late
- outputs are not organized in a way that supports disciplined IP evaluation

IdeaForge AI addresses those problems through an explicit multi-agent pipeline, observable event streaming, structured schemas, and repeatable output formats. The result is a system that is useful both as an engineering prototype and as a technical record supporting invention-management workflows.

## Patent-Support Positioning

This repository is intentionally documented at a level that supports:

- invention disclosure preparation
- technical architecture review
- novelty and differentiation discussion
- claim-oriented brainstorming support
- reduction-to-practice planning
- internal diligence for patent prosecution preparation

This does **not** mean the repository itself grants legal protection. Patent rights arise from filed and prosecuted applications under applicable law, not from README language alone. This documentation is therefore best understood as a **supporting technical record and ownership notice**, not a substitute for patent counsel, patentability opinions, or freedom-to-operate analysis.

## Core Technical Capabilities

### 1. Multi-Agent Orchestration

The pipeline is implemented with **LangGraph** and uses a typed shared state object that moves linearly through the following stages:

`START -> supervisor -> ideation -> prior_art -> synthesis -> END`

Each node is independently responsible for a well-defined phase of the workflow, which improves modularity, observability, and future extensibility.

### 2. Structured Innovation Planning

The Supervisor agent converts a free-form innovation brief into a structured plan containing:

- focus areas
- innovation angles
- validation priorities
- targeted search queries
- strategic framing

This creates a disciplined downstream handoff instead of allowing later agents to improvise without strategic alignment.

### 3. Knowledge-Graph-Augmented Ideation

The Ideation agent queries a **NetworkX** knowledge graph populated with:

- technology nodes
- domain nodes
- problem nodes
- innovation-pattern nodes
- typed edges describing relevance or leverage relationships

The agent combines graph-derived context with the Supervisor plan to generate concept candidates that are more grounded, more cross-disciplinary, and more differentiated than generic text-only prompting.

### 4. Prior-Art Screening

The Prior Art agent currently performs **academic prior-art screening** using:

- `arXiv`
- `Semantic Scholar`

For each concept, it:

- constructs a concept-level query
- retrieves candidate papers
- scores relevance with the LLM
- records key differences between the concept and the retrieved literature

This is useful for early novelty screening. It is **not yet a full patent database search** and should not be represented as a completed patentability or FTO opinion.

### 5. IP-Readiness Synthesis

The Synthesis agent produces a consolidated report containing:

- innovation concepts
- prior-art evidence
- novelty assessment
- executive summary
- IP-readiness score
- recommended next steps

This final output is designed to be readable by founders, inventors, technical reviewers, and patent counsel.

## System Architecture

```text
User Brief
   |
   v
FastAPI REST endpoint (/api/innovate)
   |
   v
LangGraph workflow
   |
   +--> Supervisor  -> strategic plan + search framing
   +--> Ideation    -> knowledge-graph-augmented concept generation
   +--> Prior Art   -> academic prior-art retrieval + relevance scoring
   +--> Synthesis   -> novelty report + IP-readiness synthesis
   |
   v
WebSocket event stream (/ws/{session_id})
   |
   v
Frontend dashboard (live progress + final report)
```

## Component-Level Design

### Backend

The backend is a FastAPI application that exposes:

- `POST /api/innovate` to launch a run
- `GET /api/health` for status and demo-mode visibility
- `GET /api/session` to create a client session identifier
- `WS /ws/{session_id}` for live event streaming

The backend also:

- pre-warms the LangGraph workflow at startup
- serves the frontend as static assets
- maintains per-session event queues for real-time progress streaming
- supports both live mode and deterministic mock/demo mode

### Frontend

The frontend is intentionally lightweight and framework-free:

- `frontend/index.html` defines the application shell
- `frontend/styles.css` provides the interactive dashboard styling
- `frontend/app.js` handles form submission, WebSocket events, partial rendering, and final report display

The UI visualizes pipeline state, logs incremental execution updates, and renders concept cards, prior-art blocks, and the final novelty/IP report.

### Shared State and Event Model

The LangGraph state includes:

- user inputs (`domain`, `problem_space`, `user_intent`, `depth`)
- cumulative messages
- structured supervisor plan
- innovation concepts
- prior-art results
- novelty assessment
- executive summary
- IP-readiness score
- next steps
- internal execution metadata

The event stream includes:

- `agent_start`
- `agent_progress`
- `agent_complete`
- `pipeline_complete`
- `error`

This makes the workflow observable and suitable for future audit logging or persistence.

## Repository Structure

```text
code_agent_1_ideation_to_IP/
|- backend/
|  |- agents/
|  |  |- supervisor.py
|  |  |- ideation.py
|  |  |- prior_art.py
|  |  `- synthesis.py
|  |- graph/
|  |  `- workflow.py
|  |- knowledge/
|  |  |- domain_data.py
|  |  `- knowledge_graph.py
|  |- models/
|  |  `- schemas.py
|  |- tools/
|  |  |- arxiv_search.py
|  |  `- semantic_scholar.py
|  |- config.py
|  |- events.py
|  |- main.py
|  `- requirements.txt
|- frontend/
|  |- index.html
|  |- styles.css
|  `- app.js
|- .env.example
`- README.md
```

## Runtime Modes

### Live Mode

Live mode is enabled when `OPENAI_API_KEY` is present in `.env`.

Characteristics:

- real LLM calls
- real academic search calls
- realistic novelty scoring
- variable latency and API cost

### Demo Mode

Demo mode is enabled when `OPENAI_API_KEY` is missing or placeholder text is used.

Characteristics:

- deterministic mock plans
- mock innovation concepts
- mock prior-art blocks
- mock final report
- zero OpenAI cost

This is useful for demos, UI development, and offline walkthroughs.

## Setup and Installation

### Prerequisites

- Python 3.10+ recommended
- Internet connectivity for live-mode LLM and literature search calls
- Valid OpenAI API key for live mode

### 1. Clone and create the virtual environment

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

macOS / Linux equivalent:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment variables

From repository root:

```powershell
copy .env.example .env
```

or:

```bash
cp .env.example .env
```

Then set values such as:

- `OPENAI_API_KEY`
- `OPENAI_MODEL`
- `ARXIV_MAX_RESULTS`
- `SEMANTIC_SCHOLAR_MAX_RESULTS`
- `APP_HOST`
- `APP_PORT`

### 3. Run the application

From the repository root:

```powershell
cd backend
.\.venv\Scripts\uvicorn.exe main:app --host 0.0.0.0 --port 8000 --reload
```

Then open:

`http://localhost:8000`

## API Contract

### Start a pipeline

`POST /api/innovate`

Request body:

```json
{
  "session_id": "uuid-string",
  "domain": "Healthcare AI",
  "problem_space": "Clinical decision support with auditability requirements",
  "user_intent": "Generate differentiated, patent-supportive innovation concepts",
  "depth": "standard"
}
```

Response body:

```json
{
  "status": "started",
  "session_id": "uuid-string",
  "demo_mode": true
}
```

### Request a fresh session id

`GET /api/session`

### Health check

`GET /api/health`

## WebSocket Contract

Connect to:

`/ws/{session_id}`

Representative event:

```json
{
  "type": "agent_complete",
  "agent": "ideation",
  "message": "3 innovation concepts generated.",
  "data": {
    "concepts": []
  },
  "timestamp": 1712360000.0
}
```

## Engineering Notes

### Reliability Improvements Already Applied

The current codebase includes several practical improvements to strengthen runtime behavior:

- per-session event queues are created early so initial agent events are less likely to be lost during WebSocket connection race conditions
- request payloads are validated more strictly at the API boundary
- mock outputs are deep-copied so repeated runs do not mutate shared in-memory fixtures
- paper scoring is executed concurrently for better prior-art throughput

### Extensibility Paths

This system is intentionally modular. High-value next steps include:

- integrating patent databases such as USPTO, Google Patents, EPO, or Lens
- persisting run outputs to a database or object store
- adding citation export, PDF generation, or invention disclosure packet generation
- introducing claim-template generation or embodiment clustering
- adding authentication, access controls, and audit logs
- adding benchmark datasets for novelty-analysis quality evaluation

## Limitations

This repository should be used with clear expectations:

- current prior-art search is academic-first, not patent-database-complete
- output quality depends on upstream prompt quality and model behavior
- novelty scores are advisory heuristics, not legal determinations
- the system is an invention-support tool, not a substitute for patent prosecution, legal review, or jurisdiction-specific filing strategy

## Intellectual Property and Patent Notice

The solution embodied in this repository is the property of **Yang (Rick) Wang, Ph.D.** The source code, prompts, agent workflow definitions, architecture descriptions, technical documentation, and associated implementation materials are proprietary and confidential to the extent preserved by applicable law and handling practices.

This repository is maintained in a manner consistent with support for **already-filed patent application(s)** and related patent-pending subject matter. The presence of technical detail in this README or the repository should be interpreted as:

- notice of ownership
- notice of reserved rights
- notice that patent-related subject matter may already be on file
- notice that access is not permission

It should **not** be interpreted as:

- an open-source grant
- a patent license
- a copyright license
- a waiver of claims
- a freedom-to-operate opinion
- legal advice

If this repository is shared with collaborators, reviewers, or prospective partners, that sharing should occur only under terms consistent with the owner's intended IP strategy and any guidance from patent counsel.

## Use Restrictions

Unless expressly authorized in writing by **Yang (Rick) Wang, Ph.D.**, you may not:

- copy substantial portions of the proprietary implementation
- reuse the architecture as a commercial derivative
- reproduce the prompts, workflows, or technical documentation for competing products
- distribute the repository or derived proprietary materials
- remove authorship or ownership attribution
- represent the work as public-domain or open-source

## Attribution Requirement

Any authorized internal or external reference to this system should preserve attribution to:

**Yang (Rick) Wang, Ph.D.**

## Final Disclaimer

This repository is an engineering and invention-support artifact. It is intended to help structure technical thinking, document differentiators, and support discussions around innovation and patent strategy. It is **not** a substitute for advice from a qualified patent attorney or agent, and it does not by itself create or guarantee enforceable patent rights in any jurisdiction.
