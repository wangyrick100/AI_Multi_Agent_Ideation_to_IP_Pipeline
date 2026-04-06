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

## Patent-Core File Status

This `README.md` is intended to function as the **master technical disclosure file** for this solution and as the central working document from which patent counsel or a patent drafting team can prepare a provisional filing package, a nonprovisional specification package, continuation support materials, invention disclosure memoranda, and supporting figures.

For that purpose, this README is structured to support:

- invention title and technical field identification
- background problem framing
- written-description support
- enablement-oriented technical disclosure
- preferred-embodiment documentation
- alternative embodiments and design-around coverage
- figure-planning guidance
- claim-drafting support
- inventor/ownership attribution

This README should therefore be treated as the **core disclosure record**, while recognizing that a formal U.S. patent application still requires separate filing components such as formal claims, drawings where necessary, cover-sheet / ADS materials, declarations where applicable, and practitioner review.

## Document Control

- Disclosure title: **Multi-Agent Innovation-to-IP Pipeline with Knowledge-Graph-Augmented Ideation, Prior-Art Screening, and IP-Readiness Synthesis**
- Inventor / owner: **Yang (Rick) Wang, Ph.D.**
- Document role: **Master patent-support disclosure file**
- Repository role: **Primary engineering embodiment and reduction-to-practice support**
- Current status: **Patent-pending / already-filed subject matter reflected**
- Confidentiality posture: **Proprietary; distribute only in a manner consistent with patent strategy**

## Invention Title

**Systems and Methods for Multi-Agent Innovation Analysis, Knowledge-Graph-Augmented Ideation, Prior-Art-Aware Concept Generation, and IP-Readiness Synthesis**

## Patent Abstract

Disclosed are systems, methods, and computer-readable media for transforming an unstructured innovation brief into a structured invention-oriented output using a coordinated plurality of software agents. In one embodiment, a supervisor agent converts free-form user input into a strategic plan comprising focus areas, innovation angles, validation priorities, and search queries. An ideation agent then combines the strategic plan with knowledge-graph-derived context to produce differentiated technical concepts. A prior-art agent retrieves and scores literature evidence against the generated concepts, and a synthesis agent produces a novelty-oriented output package including concept summaries, differentiators, risk areas, and IP-readiness recommendations. The disclosed architecture improves repeatability, traceability, and technical rigor in early-stage invention development and can be implemented as a server-executed workflow with real-time event streaming to a client interface.

## Technical Field

The disclosed subject matter generally relates to:

- artificial intelligence systems
- multi-agent software orchestration
- knowledge-graph-assisted reasoning
- innovation management and invention support systems
- prior-art-informed concept generation
- computer-implemented patent-support workflows

More particularly, the disclosure concerns computer-implemented systems and methods for converting unstructured innovation intent into structured, technically differentiated, novelty-aware invention outputs.

## Background and Technical Problem

Conventional ideation workflows suffer from a recurring set of deficiencies that reduce patent quality and make invention capture inconsistent:

- valuable invention ideas originate in unstructured notes, chats, or meetings and are not normalized into reusable technical records
- brainstorming systems often generate generic ideas that are weakly differentiated and poorly grounded in real technical constraints
- prior-art diligence is often delayed, shallow, or disconnected from the concept-generation stage
- innovation outputs rarely map cleanly into written-description, enablement, embodiment, and claim-development workflows
- inventors and counsel frequently lose time reconstructing architecture, alternatives, and inventive step after the engineering work is already underway

Accordingly, there is a need for a computer-implemented system that can systematically ingest innovation intent, reason across structured technical knowledge, generate differentiated embodiments, compare them against relevant prior art, and synthesize outputs into a format suitable for invention disclosure and patent-preparation workflows.

## Problem-Solution Statement

The present solution addresses the foregoing problems by introducing an orchestrated multi-agent pipeline in which:

1. a first agent structures the innovation problem and determines downstream exploration strategy,
2. a second agent generates concept candidates using both model reasoning and a knowledge graph,
3. a third agent performs relevance-oriented prior-art screening against generated concepts, and
4. a fourth agent synthesizes the results into a novelty-aware invention support report.

This coordinated architecture produces a more defensible and more reproducible invention-development workflow than conventional brainstorming or isolated retrieval systems.

## Written-Description-Oriented Summary of the Invention

In one aspect, the invention provides a **computer-implemented system** comprising:

- a server system executing a workflow engine
- a shared state object storing innovation inputs and intermediate outputs
- a supervisor agent configured to generate structured planning data from an innovation brief
- an ideation agent configured to generate one or more candidate technical concepts using the planning data and graph-derived context
- a prior-art agent configured to retrieve and score external literature evidence responsive to the candidate concepts
- a synthesis agent configured to produce a structured novelty and IP-readiness output
- an event-streaming subsystem configured to transmit intermediate workflow events to a client device

In another aspect, the invention provides a **computer-implemented method** comprising:

- receiving an innovation brief from a client system
- generating structured planning output from the innovation brief
- extracting graph-relevant context from a domain knowledge representation
- generating candidate invention concepts based on the planning output and graph context
- retrieving prior-art references responsive to the candidate invention concepts
- scoring relevance of the prior-art references to the candidate invention concepts
- synthesizing a final invention-support report comprising novelty indicators and recommended next actions

In another aspect, the invention provides a **non-transitory computer-readable medium** storing instructions that cause one or more processors to perform the foregoing method.

## Inventive Concepts and Novelty Themes

The presently disclosed implementation supports at least the following inventive themes, alone or in combination:

- use of a multi-agent sequence to convert unstructured invention intent into a structured IP-support output
- use of a knowledge graph as an ideation-grounding layer rather than merely as a passive metadata store
- use of prior-art retrieval and LLM-based relevance scoring as part of the invention-generation loop
- use of a synthesis layer that outputs novelty, risk, and next-step data in a format optimized for patent preparation
- use of live event streaming to preserve transparency and traceability across the innovation workflow

## Best-Mode / Preferred Embodiment Overview

The presently contemplated preferred embodiment is the implementation contained in this repository:

- **FastAPI** backend for API and WebSocket transport
- **LangGraph** for agent orchestration
- **OpenAI-compatible chat models** for structured planning, ideation, scoring, and synthesis
- **NetworkX** knowledge graph for domain, problem, pattern, and technology reasoning
- **arXiv** and **Semantic Scholar** connectors for literature retrieval
- browser-based interface for human review and event visibility

This embodiment is preferred because it is modular, inspectable, operationally lightweight, and already reduced to a working prototype that demonstrates practical implementation of the disclosed architecture.

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

This does **not** mean the repository itself grants legal protection. Patent rights arise from filed and prosecuted applications under applicable law, not from README language alone. This documentation is therefore best understood as a **supporting technical record and ownership notice**, and as the primary technical disclosure file for filing preparation, not a substitute for patent counsel, patentability opinions, or freedom-to-operate analysis.

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

## Detailed Description of the Preferred Embodiment

### A. Input Acquisition Layer

In the preferred embodiment, a client interface receives an innovation brief containing at least:

- a target domain
- a problem space
- a statement of user intent
- an optional depth parameter

The input is transmitted to a backend service through a REST endpoint and associated with a session identifier. The session identifier is used to coordinate background execution and event-stream delivery.

### B. Workflow Orchestration Layer

The backend initializes a graph-based workflow that maintains a shared state structure. The shared state carries input variables, intermediate agent outputs, and final synthesis results across the lifecycle of a single innovation session.

The workflow executes a plurality of nodes in sequence, including at least:

- a supervisor node
- an ideation node
- a prior-art node
- a synthesis node

In variants, the workflow may be linear, branching, iterative, conditional, human-gated, or confidence-threshold-based.

### C. Supervisor Agent

The supervisor agent receives the innovation brief and transforms it into structured planning data. In the current embodiment, the planning data includes:

- focus areas
- innovation angles
- validation priorities
- search queries
- strategic framing

This transformation improves downstream consistency by constraining later stages to a shared analytical frame.

### D. Knowledge Graph Layer

The knowledge graph stores a structured taxonomy of:

- technology nodes
- domain nodes
- problem nodes
- innovation-pattern nodes
- typed edges connecting the foregoing

The graph is queried using normalized domain and problem keywords extracted from the user brief. Inferred domain matches may also be derived from matched problem nodes. The graph returns context relevant to potential technologies, applicable patterns, and adjacent areas for cross-domain transfer.

### E. Ideation Agent

The ideation agent consumes:

- user-provided domain and problem information
- supervisor planning data
- knowledge-graph context

The ideation agent generates a set of candidate technical concepts, each preferably comprising:

- title
- description
- technical approach
- use cases
- implementation pathway
- strategic positioning
- novelty indicators

In this manner, the ideation stage is not purely generative. Rather, it is conditioned on a structured planning layer and a graph-based grounding layer.

### F. Prior-Art Agent

The prior-art agent generates concept-linked search activity and retrieves literature results from one or more external data sources. In the presently implemented embodiment, those sources include arXiv and Semantic Scholar.

The prior-art agent may:

- construct or select a concept-level query
- retrieve candidate references
- normalize metadata
- score concept-to-reference relevance
- describe key differences between the concept and the retrieved reference

In other embodiments, the same architectural role may be extended to patent databases, enterprise literature stores, or private corpora.

### G. Synthesis Agent

The synthesis agent aggregates upstream outputs and produces a final invention-support package. In the preferred embodiment, that package includes:

- innovation concepts
- prior-art result groupings
- novelty assessment
- executive summary
- IP-readiness score
- recommended next actions

The synthesis output is structured so it can be used for invention review, claim brainstorming, diligence discussions, and patent-counsel handoff.

### H. Event Streaming and User Interface

The system further includes a WebSocket event-streaming layer configured to publish intermediate workflow events to a client device. This enables:

- run-time transparency
- stage-by-stage review
- auditability of workflow progression
- rapid human intervention or interpretation

The interface may display agent state, logs, concepts, prior-art evidence, novelty output, and filing-oriented next steps.

## Method Disclosure

An example method supported by the present disclosure comprises:

1. receiving, at a server, an innovation brief from a client device;
2. generating, by a supervisor agent, structured plan data from the innovation brief;
3. identifying, from a knowledge graph, domain, problem, technology, and/or innovation-pattern context associated with the innovation brief;
4. generating, by an ideation agent, one or more candidate technical concepts using the structured plan data and the knowledge-graph context;
5. retrieving, by a prior-art agent, one or more references associated with the one or more candidate technical concepts;
6. scoring relevance between the one or more candidate technical concepts and the one or more references;
7. generating, by a synthesis agent, a structured novelty and IP-readiness output; and
8. transmitting intermediate and/or final workflow outputs to a client device.

Additional method variations may include:

- iterative refinement loops
- human review checkpoints
- confidence-threshold branching
- claim-generation subroutines
- patent-database retrieval
- persistence into invention-management systems

## Alternative Embodiments and Variations

Without limitation, the disclosed system may be varied in any of the following ways while remaining within the inventive concept:

- replacing the LLM provider while preserving the multi-agent workflow architecture
- replacing the graph implementation with another graph database or semantic layer
- adding iterative loops between prior-art retrieval and ideation
- integrating patent databases, legal datasets, or enterprise knowledge bases
- generating one concept or more than three concepts
- producing claim charts, embodiments, figures, or inventor questionnaires as additional outputs
- executing the agents on one machine, multiple services, or cloud-native distributed infrastructure
- replacing the browser client with an API-only integration, IDE plugin, or enterprise portal

## Industrial Applicability

The disclosed system is industrially applicable to at least:

- innovation management
- corporate R&D
- university technology transfer
- startup invention capture
- internal prior-art screening
- patent-counsel intake workflows
- regulated-industry invention evaluation

## Advantages Over Conventional Approaches

Compared with ordinary brainstorming tools or simple retrieval systems, the present disclosure provides:

- better structure and repeatability
- tighter linkage between ideation and novelty review
- graph-grounded technical context
- clearer embodiment capture
- improved traceability for invention-development history
- outputs that are substantially closer to patent-preparation format

## Figure Package Guidance

For filing support, the following figures are recommended as a companion drawing set derived from this README:

- **FIG. 1**: High-level system architecture showing client, API layer, workflow engine, knowledge graph, external search sources, and output interface
- **FIG. 2**: Workflow diagram showing supervisor, ideation, prior-art, and synthesis stages
- **FIG. 3**: Data-flow diagram showing movement of the shared state through the workflow
- **FIG. 4**: Knowledge-graph schema showing technology, domain, problem, and innovation-pattern nodes and typed edges
- **FIG. 5**: Example method flow for generating invention-support outputs from an innovation brief
- **FIG. 6**: Example user interface showing live stage execution and final novelty-oriented output
- **FIG. 7**: Example concept-to-prior-art scoring pipeline
- **FIG. 8**: Example synthesis report structure

## Claim-Drafting Support

The present disclosure supports drafting at least the following claim families:

- **System claims** directed to a multi-agent innovation analysis system
- **Method claims** directed to transforming an innovation brief into a novelty-aware output through a plurality of coordinated agents
- **Computer-readable medium claims** directed to instructions that implement the workflow
- **Subcombination claims** directed to the knowledge-graph-augmented ideation layer, the prior-art scoring layer, or the synthesis layer individually

Potential independent-claim themes include:

- a server-implemented multi-agent workflow with shared state propagation
- graph-conditioned concept generation responsive to structured planning data
- prior-art-informed concept scoring and differentiation
- event-streamed invention-support output generation

Potential dependent-claim themes include:

- use of domain, problem, pattern, and technology nodes
- typed graph edges for domain inference
- dynamic query construction for literature retrieval
- concept-level relevance scoring using language models
- generation of novelty indicators, risk areas, and filing recommendations
- real-time event streaming to a remote user interface
- configurable run depth or human-in-the-loop review stages

## Patent Filing Handoff Checklist

When using this README as the core patent-support file, the following items should be prepared or verified before filing:

- inventor list and inventorship review
- assignee / ownership chain review
- application type decision: provisional, nonprovisional, continuation, or CIP
- formal figure set based on the figure guidance above
- independent and dependent claims prepared by counsel or drafting team
- abstract finalized to filing format
- title harmonized with filing strategy
- consistency check against any already-filed application to avoid unintended divergence
- review for confidential matter and third-party content
- evidence package retained for reduction to practice, if available

## USPTO Alignment Notes

This README is structured to help align with patent drafting needs reflected in official USPTO guidance, including:

- written description / enablement / best-mode-oriented disclosure under 35 U.S.C. 112(a)
- the fact that a provisional application does not require claims, but still benefits from a complete technical disclosure
- the need for drawings when necessary for understanding the invention

Official references:

- USPTO MPEP on provisional applications: <https://www.uspto.gov/web/offices/pac/mpep/documents/0200_201_11.htm>
- USPTO provisional application overview: <https://www.uspto.gov/patents-getting-started/patent-basics/types-patent-applications/provisional-application-patent>
- USPTO MPEP discussion of best mode and enablement: <https://www.uspto.gov/web/offices/pac/mpep/documents/2100_2165_04.htm>
- USPTO guidance on written description support and prohibition on adding new matter: <https://www.uspto.gov/web/offices/pac/mpep/documents/2100_2163.htm> and <https://www.uspto.gov/web/offices/pac/mpep/documents/2100_2163_06.htm>

These references support using this README as a **core technical disclosure document**, but not as a substitute for the complete formal filing package itself. If this README is used to support a filing strategy tied to an already-filed application, later README expansions should be reviewed carefully so they are not mistaken for subject matter that was part of the original filed disclosure.

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
