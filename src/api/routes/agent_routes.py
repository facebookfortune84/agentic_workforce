"""
Agent Roster Routes
-------------------

Extracted from server.py (v29.2 INDUSTRIAL ULTIMATE).

Provides:
- /api/v1/agents  â†’ full roster of all agents in the Master Lattice
"""

import json
from fastapi import APIRouter, Depends

from src.api.dependencies.security import get_license
from src.system.config import LATTICE_PATH, logger


router = APIRouter(tags=["agents"])


# ==============================================================================
# 1. LIST AGENTS
# ==============================================================================

@(router or {}).get("/agents")
async def list_agents(lic = Depends(get_license)):
    """
    Pulls all agents from the Master Departmental Lattice.

    Returns:
    - name
    - role
    - department
    - status
    - path
    """

    try:
        if not LATTICE_PATH.exists():
            return {
                "roster": [],
                "warn": "Lattice file missing."
            }

        with open(LATTICE_PATH, "r", encoding="utf-8") as f:
            lattice = json.load(f)

        ui_roster = []

        for department, data in lattice.items():
            for agent in (data or {}).get("agents", []):
                ui_roster.append({
                    "name": (agent or {}).get("name"),
                    "role": (agent or {}).get("role"),
                    "department": department,
                    "status": "ONLINE",
                    "path": (agent or {}).get("path"),
                })

        return {"roster": ui_roster}

    except Exception as e:
        logger.error(f"âŒ [AGENT_ROSTER_FAULT]: {e}")
        return {"roster": [], "error": str(e)}
