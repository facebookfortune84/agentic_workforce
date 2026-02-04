"""
RealmForge Sovereign Gateway â€” Application Entrypoint
-----------------------------------------------------

This file replaces the legacy monolithic server.py.

Responsibilities:
- FastAPI app creation
- Lifespan boot sequence
- Genesis Engine initialization
- Static file mounting
- CORS configuration
- Router registration
- WebSocket endpoint registration
"""

import os
import time
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from contextlib import asynccontextmanager

from src.system.config import (
    STATIC_PATH,
    logger,
)
from src.api.dependencies.security import get_license
from src.system.connection_manager import manager
from src.auth import gatekeeper


# ==============================================================================
# 1. GENESIS ENGINE LOADER
# ==============================================================================

genesis_engine = None

def get_brain():
    """
    Lazily loads the Genesis Engine (realm_core.app).
    This mirrors the behavior from server.py.
    """
    global genesis_engine

    if genesis_engine is None:
        try:
            logger.info("ðŸ§  [BRAIN] Awakening Genesis Engine...")
            from realm_core import app as brain_app
            genesis_engine = brain_app
            logger.info("âœ… [BRAIN] Genesis Engine Online.")
        except Exception as e:
            logger.error(f"âŒ [CRITICAL] Engine Fault: {e}")
            raise RuntimeError(f"Engine Failed to Ignite: {e}")

    return genesis_engine


# ==============================================================================
# 2. LIFESPAN CONTEXT
# ==============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Boot sequence executed when the FastAPI app starts.
    """
    # Initialize Genesis Engine
    get_brain()

    # Initialize Gatekeeper auth DB
    await gatekeeper.init_auth_db()

    cid = os.getenv("GITHUB_CLIENT_ID")
    ruri = os.getenv("GITHUB_REDIRECT_URI", "http://localhost:8000/api/v1/auth/github/callback")
    debug_url = (
        f"https://github.com/login/oauth/authorize?"
        f"client_id={cid}&redirect_uri={ruri}&scope=repo,user"
    )

    print("\n" + "ðŸš€" * 20, flush=True)
    print("âœ… [BRAIN] TITAN-INDUSTRIAL HUD ONLINE.", flush=True)
    print("âœ… [LATTICE] SOVEREIGN NODE READY ON PORT 8000.", flush=True)
    print(f"ðŸŒ€ [INTELLIGENCE] Mode: {os.getenv('REALM_MODEL_CORE', 'GROQ')}", flush=True)
    print(f"ðŸ—ï¸ [OAUTH DEBUG LINK]: {debug_url}", flush=True)
    print("ðŸš€" * 20 + "\n", flush=True)

    yield

    logger.info("ðŸ”Œ [OFFLINE] Sovereign Node shutdown initiated.")


# ==============================================================================
# 3. FASTAPI APP INITIALIZATION
# ==============================================================================

app = FastAPI(
    title="RealmForge OS - Sovereign Gateway",
    version="29.2.0",
    lifespan=lifespan
)

# Static file mount
app.mount("/static", StaticFiles(directory=str(STATIC_PATH)), name="static")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


# ==============================================================================
# 4. PRE-FLIGHT HANDLER
# ==============================================================================

@app.options("/{rest_of_path:path}")
async def preflight_handler(request: Request, rest_of_path: str):
    return {}


# ==============================================================================
# 5. ROUTER REGISTRATION
# ==============================================================================

from src.api.routes import (
    auth_routes,
    assistant_routes,
    mission_routes,
    io_routes,
    agent_routes,
    graph_routes,
    stt_routes,
)

app.include_router(auth_routes.router, prefix="/api/v1/auth")
app.include_router(assistant_routes.router, prefix="/api/v1/assistant")
app.include_router(mission_routes.router, prefix="/api/v1")
app.include_router(io_routes.router, prefix="/api/v1/io")
app.include_router(agent_routes.router, prefix="/api/v1")
app.include_router(graph_routes.router, prefix="/api/v1")
app.include_router(stt_routes.router, prefix="/api/v1")


# ==============================================================================
# 6. HEALTH CHECK
# ==============================================================================

from datetime import datetime

@app.get("/health")
def health():
    return {"status": "ONLINE", "timestamp": datetime.now().isoformat()}


# ==============================================================================
# 7. WEBSOCKET ENDPOINT
# ==============================================================================

@app.websocket("/ws/telemetry")
async def ws_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
