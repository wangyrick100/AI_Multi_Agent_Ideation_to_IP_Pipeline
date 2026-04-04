"""
FastAPI application entry-point.

WebSocket route:  /ws/{session_id}          — real-time event stream
REST route:       POST /api/innovate         — start a pipeline run
REST route:       GET  /api/health           — health check
Static files:     /                          — frontend (../frontend/)
"""
from __future__ import annotations
import asyncio
import logging
import os
import sys
import time
import uuid
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import BackgroundTasks, FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

import events as ev
from config import APP_HOST, APP_PORT, USE_MOCK
from graph.workflow import get_graph, make_initial_state
from models.schemas import InnovationRequest

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# Pre-warm the graph at startup to avoid cold-build latency on first request
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Warming up LangGraph pipeline…")
    get_graph()
    mode = "DEMO (mock)" if USE_MOCK else "LIVE (OpenAI)"
    logger.info("Pipeline ready — running in %s mode.", mode)
    yield


app = FastAPI(
    title="AI Innovation Pipeline",
    description="Multi-agent ideation → prior-art → IP-readiness system",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ──────────────────────────────────────────────────────────────────────────────
# WebSocket endpoint — streams agent events to the browser
# ──────────────────────────────────────────────────────────────────────────────
@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    channel = ev.create_channel(session_id)
    logger.info("WS opened: %s", session_id)
    try:
        while True:
            try:
                msg = await asyncio.wait_for(channel.get(), timeout=300.0)
            except asyncio.TimeoutError:
                await websocket.send_json({"type": "ping"})
                continue

            if msg is None:          # sentinel — pipeline finished
                break

            await websocket.send_json(msg)

            if msg.get("type") == "pipeline_complete":
                break
    except WebSocketDisconnect:
        logger.info("WS client disconnected: %s", session_id)
    except Exception as exc:
        logger.error("WS error for %s: %s", session_id, exc)
    finally:
        ev.remove_channel(session_id)
        try:
            await websocket.close()
        except Exception:
            pass
        logger.info("WS closed: %s", session_id)


# ──────────────────────────────────────────────────────────────────────────────
# REST endpoint — launches pipeline as a background task
# ──────────────────────────────────────────────────────────────────────────────
@app.post("/api/innovate")
async def start_pipeline(request: InnovationRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(_run_pipeline, request)
    return {"status": "started", "session_id": request.session_id, "demo_mode": USE_MOCK}


async def _run_pipeline(request: InnovationRequest) -> None:
    session_id = request.session_id
    try:
        initial_state = make_initial_state(
            session_id=session_id,
            domain=request.domain,
            problem_space=request.problem_space,
            user_intent=request.user_intent,
            depth=request.depth,
        )
        graph = get_graph()
        async for _step in graph.astream(initial_state):
            pass   # events are emitted inside agent nodes via ev.emit()
    except Exception as exc:
        logger.error("Pipeline error for session %s: %s", session_id, exc, exc_info=True)
        await ev.emit(session_id, {
            "type":    "error",
            "agent":   "system",
            "message": f"Pipeline error: {exc}",
        })
    finally:
        await ev.close_session(session_id)


# ──────────────────────────────────────────────────────────────────────────────
# Utility endpoints
# ──────────────────────────────────────────────────────────────────────────────
@app.get("/api/health")
async def health():
    return {"status": "ok", "demo_mode": USE_MOCK, "timestamp": time.time()}


@app.get("/api/session")
async def new_session():
    """Generate a fresh session UUID for the client."""
    return {"session_id": str(uuid.uuid4())}


# ──────────────────────────────────────────────────────────────────────────────
# Static frontend — must come last so API routes take priority
# ──────────────────────────────────────────────────────────────────────────────
_frontend_dir = Path(__file__).parent.parent / "frontend"
if _frontend_dir.exists():
    app.mount("/", StaticFiles(directory=str(_frontend_dir), html=True), name="static")
else:
    logger.warning("Frontend directory not found at %s — static serving disabled.", _frontend_dir)


# ──────────────────────────────────────────────────────────────────────────────
# Dev-server entry-point
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=APP_HOST,
        port=APP_PORT,
        reload=True,
        log_level="info",
    )
