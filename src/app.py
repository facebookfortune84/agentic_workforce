"""
RealmForge Sovereign Gateway — Application Entrypoint
-----------------------------------------------------
PATH: backend/server.py (or your entry point)
"""

import os
import time
import traceback
import sys
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from src.system.config import STATIC_PATH, logger
from src.api.dependencies.security import get_license
from src.system.connection_manager import manager
from src.auth import gatekeeper

# ==============================================================================
# 1. GENESIS ENGINE LOADER
# ==============================================================================
genesis_engine = None

def get_brain():
    global genesis_engine
    if genesis_engine is None:
        try:
            logger.info("🧠 [BRAIN] Awakening Genesis Engine...")
            from realm_core import app as brain_app
            genesis_engine = brain_app
            logger.info("✅ [BRAIN] Genesis Engine Online.")
        except Exception as e:
            logger.error(f"❌ [CRITICAL] Engine Fault: {e}")
            raise RuntimeError(f"Engine Failed to Ignite: {e}")
    return genesis_engine

# ==============================================================================
# 2. LIFESPAN CONTEXT
# ==============================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    get_brain()
    await gatekeeper.init_auth_db()

    cid = os.getenv("GITHUB_CLIENT_ID")
    ruri = os.getenv("GITHUB_REDIRECT_URI", "http://localhost:8000/api/v1/auth/github/callback")
    debug_url = f"https://github.com/login/oauth/authorize?client_id={cid}&redirect_uri={ruri}&scope=repo,user"

    print("\n" + "🚀" * 20, flush=True)
    print("✅ [BRAIN] TITAN-INDUSTRIAL HUD ONLINE.", flush=True)
    print("✅ [LATTICE] SOVEREIGN NODE READY ON PORT 8000.", flush=True)
    print(f"🌀 [INTELLIGENCE] Mode: {os.getenv('REALM_MODEL_CORE', 'GROQ')}", flush=True)
    print(f"🛰️  [OAUTH DEBUG LINK]: {debug_url}", flush=True)
    print("🚀" * 20 + "\n", flush=True)

    yield
    logger.info("🔌 [OFFLINE] Sovereign Node shutdown initiated.")

# ==============================================================================
# 3. FASTAPI APP INITIALIZATION
# ==============================================================================
app = FastAPI(
    title="RealmForge OS - Sovereign Gateway",
    version="29.2.0",
    lifespan=lifespan
)

# --- AUTO-HEAL MIDDLEWARE: ONE-PUNCH RUNTIME FIXER ---
@app.middleware("http")
async def catch_none_errors_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        # Intercept the specific 'NoneType' has no attribute 'get' error
        if "'NoneType' object has no attribute 'get'" in str(e):
            print("\n" + "🛑" * 30)
            print("REALM FORGE CRITICAL FAULT: NONE-TYPE COLLISION DETECTED")
            print("-" * 60)
            exc_type, exc_value, exc_traceback = sys.exc_info()
            tb = traceback.extract_tb(exc_traceback)[-1]
            print(f"FILE: {tb.filename}")
            print(f"LINE: {tb.lineno}")
            print(f"CODE: {tb.line}")
            print("-" * 60)
            print("HEALING LOGIC: This happens when the LLM returns bad JSON or an Agent is missing.")
            print("🛑" * 30 + "\n")
            
            return JSONResponse(
                status_code=500,
                content={"status": "FAULT", "message": f"Neural Link Depressurized at {tb.filename}:{tb.lineno}"}
            )
        raise e

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
# 4. ENDPOINTS
# ==============================================================================
@app.get("/")
async def root_gateway():
    return {
        "status": "ONLINE",
        "node": "TITAN-INDUSTRIAL-CORE",
        "version": "29.2.0"
    }

@app.options("/{rest_of_path:path}")
async def preflight_handler(request: Request, rest_of_path: str):
    return {}

# --- ROUTER REGISTRATION ---
from src.api.routes import (
    auth_routes, assistant_routes, mission_routes,
    io_routes, agent_routes, graph_routes, stt_routes,
)

app.include_router(auth_routes.router, prefix="/api/v1/auth")
app.include_router(assistant_routes.router, prefix="/api/v1/assistant")
app.include_router(mission_routes.router, prefix="/api/v1")
app.include_router(io_routes.router, prefix="/api/v1/io")
app.include_router(agent_routes.router, prefix="/api/v1")
app.include_router(graph_routes.router, prefix="/api/v1")
app.include_router(stt_routes.router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "ONLINE", "timestamp": datetime.now().isoformat()}

@app.websocket("/ws/telemetry")
async def ws_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)