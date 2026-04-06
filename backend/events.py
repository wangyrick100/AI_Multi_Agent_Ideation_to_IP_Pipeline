"""
Async event channel manager for WebSocket streaming.

Each active pipeline session has its own asyncio.Queue.
Agent nodes put messages into the queue; the WebSocket handler
reads and forwards them to the client in real time.
"""
from __future__ import annotations
import asyncio
import time
from typing import Any, Dict, Optional

_channels: Dict[str, asyncio.Queue] = {}


def create_channel(session_id: str) -> asyncio.Queue:
    """Return the existing session queue or create it on first use."""
    queue = _channels.get(session_id)
    if queue is None:
        queue = asyncio.Queue()
        _channels[session_id] = queue
    return queue


def get_channel(session_id: str) -> Optional[asyncio.Queue]:
    return _channels.get(session_id)


def remove_channel(session_id: str) -> None:
    _channels.pop(session_id, None)


async def emit(session_id: str, message: Dict[str, Any]) -> None:
    """Put a message into the session channel (non-blocking for callers)."""
    channel = _channels.get(session_id)
    if channel:
        message.setdefault("timestamp", time.time())
        await channel.put(message)


async def close_session(session_id: str) -> None:
    """Signal the WebSocket reader to stop, then clean up the channel."""
    channel = _channels.get(session_id)
    if channel:
        await channel.put(None)   # sentinel – causes reader loop to exit
    remove_channel(session_id)
