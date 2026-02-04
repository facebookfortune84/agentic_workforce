"""
REALM FORGE: SOVEREIGN GATEKEEPER v22.0
ARCHITECT: LEAD SWARM ENGINEER (MASTERMIND v31.4)
STATUS: PRODUCTION READY - JWT ENGINE - ASYNC WAL - 13-SILO AUDIT ENABLED
PATH: F:/agentic_workforce_PROD/src/auth/gatekeeper.py
"""

import os
import json
import time
import uuid
import secrets
import logging
import asyncio
import aiosqlite
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Union, Any
from pydantic import BaseModel, Field
from jose import JWTError, jwt
from passlib.context import CryptContext

# --- 0. PHYSICAL PATH SOVEREIGNTY ---
ROOT_DIR = Path("F:/agentic_workforce_PROD")
BASE_PATH = ROOT_DIR / "data"
DB_PATH = BASE_PATH / "security" / "licenses.db"

# Ensure directories exist physically
os.makedirs(DB_PATH.parent, exist_ok=True)

logger = logging.getLogger("Gatekeeper")

# --- 1. SECURITY CONFIGURATION ---
MASTER_KEY = os.getenv("REALM_MASTER_KEY", "sk-realm-god-mode-888")
SECRET_KEY = os.getenv("JWT_SECRET_KEY", secrets.token_urlsafe(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 Hours for industrial uptime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ==============================================================================
# 2. DATA MODELS
# ==============================================================================

class License(BaseModel):
    """Sovereign License Model for Pydantic v2 validation."""
    key: str
    user_id: str
    tier: str  # "FREE", "PRO", "TITAN", "GOD"
    credits: int
    created_at: float
    status: str = "ACTIVE"
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None

# ==============================================================================
# 3. ASYNC DATABASE OPERATIONS (BEDROCK)
# ==============================================================================

async def init_auth_db():
    """Initializes the security database with High-Concurrency (WAL) mode."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("PRAGMA journal_mode=WAL")
        
        # Main License Table
        await db.execute('''CREATE TABLE IF NOT EXISTS licenses
                     (key text PRIMARY KEY, 
                      user_id text, 
                      tier text, 
                      credits integer, 
                      created_at real,
                      status text DEFAULT 'ACTIVE',
                      metadata text DEFAULT '{}')''')
        
        # Usage Audit Table: Expanded for 13-Silo Telemetry
        await db.execute('''CREATE TABLE IF NOT EXISTS usage_logs
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      key text,
                      agent_id text,
                      silo_id text,
                      mission_id text,
                      task_summary text,
                      cost integer,
                      timestamp real)''')
        
        await db.commit()
    logger.info(f"🔐 [GATEKEEPER] Neural Security Lattice Active (Async WAL): {DB_PATH}")

# ==============================================================================
# 4. KEY & TOKEN MANAGEMENT
# ==============================================================================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Generates a JWT for HUD authentication."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def generate_key(user_id: str, tier: str = "FREE", custom_metadata: Dict = None) -> str:
    """Mints a new high-security API Key with tier-based credits."""
    tier = tier.upper()
    prefix = f"rf_{tier.lower()}_"
    api_key = prefix + secrets.token_urlsafe(32)
    
    allotment = {
        "FREE": 100,
        "PRO": 10000,
        "TITAN": 500000,
        "GOD": 999999999
    }
    initial_credits = allotment.get(tier, 100)
    meta_json = json.dumps(custom_metadata or {})
    
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("""INSERT INTO licenses (key, user_id, tier, credits, created_at, metadata) 
                         VALUES (?, ?, ?, ?, ?, ?)""", 
                      (api_key, user_id, tier, initial_credits, time.time(), meta_json))
            await db.commit()
        logger.info(f"[NEW] [KEY_GEN] New {tier} key issued for {user_id}")
        return api_key
    except Exception as e:
        logger.error(f"[ERROR] [KEY_GEN_FAULT]: {e}")
        return None

async def validate_key(api_key: str) -> Optional[License]:
    """Validates key existence, status, and Master-Key bypass."""
    
    # 1. Master Override (God Mode)
    if api_key == MASTER_KEY:
        return License(
            key=MASTER_KEY,
            user_id="ROOT_ARCHITECT",
            tier="GOD",
            credits=999999999,
            created_at=time.time(),
            status="ACTIVE",
            metadata={"privilege": "UNRESTRICTED"}
        )

    # 2. Database Lookup
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.execute("""SELECT key, user_id, tier, credits, created_at, status, metadata 
                                   FROM licenses WHERE key=?""", (api_key,)) as cursor:
                row = await cursor.fetchone()
        
        if row:
            try: meta_dict = json.loads(row[6])
            except: meta_dict = {}

            lic = License(
                key=row[0], user_id=row[1], tier=row[2], 
                credits=row[3], created_at=row[4], status=row[5],
                metadata=meta_dict
            )
            
            if lic.status != "ACTIVE":
                logger.warning(f"🚫 [ACCESS_BLOCKED] Key {api_key[:12]}... is INACTIVE")
                return None
            return lic
            
    except Exception as e:
        logger.error(f"[ERROR] [SECURITY_FAULT]: {e}")
    
    return None

# ==============================================================================
# 5. WORKFORCE COMPLIANCE & DEDUCTION
# ==============================================================================

async def deduct_credit(api_key: str, cost: int = 1, mission_id: str = "MSN-UNK", 
                        task_context: str = "Mission", agent_id: str = "MASTERMIND",
                        silo_id: str = "Architect"):
    """
    Transactional credit deduction with high-concurrency protection.
    Tracks which of the 13 silos consumed the energy.
    """
    if api_key == MASTER_KEY:
        return True

    try:
        async with aiosqlite.connect(DB_PATH, timeout=20) as db:
            # Atomic deduction
            await db.execute("UPDATE licenses SET credits = credits - ? WHERE key = ? AND credits >= ?", 
                      (cost, api_key, cost))
            
            # Check rowcount via secondary query or last_row_id logic
            async with db.execute("SELECT changes()") as cursor:
                changes = (await cursor.fetchone())[0]

            if changes > 0:
                await db.execute("""INSERT INTO usage_logs (key, agent_id, silo_id, mission_id, task_summary, cost, timestamp) 
                             VALUES (?, ?, ?, ?, ?, ?, ?)""",
                          (api_key, agent_id, silo_id, mission_id, task_context[:200], cost, time.time()))
                await db.commit()
                return True
    except Exception as e:
        logger.error(f"[ERROR] [DEDUCTION_FAULT]: {e}")
        
    return False

async def get_account_vitals(api_key: str) -> Dict[str, Any]:
    """Retrieves account balance and workforce status for the HUD."""
    lic = await validate_key(api_key)
    if not lic:
        return {"status": "INVALID_LICENSE"}
    
    # Calculate usage stats for Bento Grid telemetry
    usage_stats = {}
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.execute("SELECT silo_id, SUM(cost) FROM usage_logs WHERE key=? GROUP BY silo_id", (api_key,)) as cursor:
                rows = await cursor.fetchall()
                usage_stats = {row[0]: row[1] for row in rows}
    except: pass

    return {
        "user_id": lic.user_id,
        "tier": lic.tier,
        "balance": lic.credits,
        "registration_status": lic.status,
        "silo_consumption": usage_stats,
        "metadata": lic.metadata
    }

# --- 6. SELF-INITIALIZATION ---
# Since this is an async-first engine, we trigger the table init
# Note: In production, server.py will call this on startup.
def bootstrap_gatekeeper():
    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.create_task(init_auth_db())
    else:
        asyncio.run(init_auth_db())

bootstrap_gatekeeper()