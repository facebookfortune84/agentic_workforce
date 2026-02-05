"""
REALM FORGE: INDUSTRIAL LEDGER v1.0
PURPOSE: Persistent logging of mission costs and specialist compensation.
PATH: F:/agentic_workforce/src/system/billing/ledger.py
"""

import aiosqlite
import time
from src.auth.gatekeeper import DB_PATH
from src.system.config import logger

class IndustrialLedger:
    @staticmethod
    async def log_mission_transaction(license_key: str, mission_id: str, agent_id: str, silo: str, cost: int):
        """Records a completed transaction to the usage_logs table."""
        try:
            async with aiosqlite.connect(DB_PATH) as db:
                await db.execute(
                    """INSERT INTO usage_logs (key, agent_id, silo_id, mission_id, task_summary, cost, timestamp) 
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (license_key, agent_id, silo, mission_id, "Completed Mission Execution", cost, time.time())
                )
                await db.commit()
            return True
        except Exception as e:
            logger.error(f"âŒ [LEDGER_FAULT] Failed to log mission {mission_id}: {e}")
            return False

    @staticmethod
    async def get_silo_usage_report(license_key: str):
        """Returns total energy consumption per silo for the UI."""
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.execute(
                "SELECT silo_id, SUM(cost) FROM usage_logs WHERE key=? GROUP BY silo_id", 
                (license_key,)
            ) as cursor:
                rows = await cursor.fetchall()
                return {row[0]: row[1] for row in rows}

