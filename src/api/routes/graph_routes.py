"""
Neural Lattice Graph Routes
---------------------------

Extracted from server.py (v29.2 INDUSTRIAL ULTIMATE).

Provides:
- /api/v1/graph â†’ returns the neural lattice graph JSON
"""

import json
from fastapi import APIRouter, Depends

from src.api.dependencies.security import get_license
from src.system.config import GRAPH_PATH, logger


router = APIRouter(tags=["graph"])


# ==============================================================================
# 1. GET LATTICE GRAPH
# ==============================================================================

@router.get("/graph")
async def get_lattice_data(lic = Depends(get_license)):
    """
    Returns the neural lattice graph used by the HUD visualization.
    """

    try:
        if not GRAPH_PATH.exists():
            return {
                "nodes": [{"id": "root", "label": "Offline"}],
                "links": []
            }

        with open(GRAPH_PATH, "r", encoding="utf-8-sig") as f:
            return json.load(f)

    except Exception as e:
        logger.error(f"âŒ [GRAPH_FAULT]: {e}")
        return {
            "nodes": [],
            "links": [],
            "error": str(e)
        }
