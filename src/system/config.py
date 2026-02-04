"""
RealmForge System Configuration
-------------------------------

Centralizes paths, logging, lattice graph path, and audit ledger.
"""

import logging
from pathlib import Path
import json

# Root anchor
ROOT_DIR = Path("F:/agentic_workforce")
DATA_ROOT = ROOT_DIR / "data"
GRAPH_PATH = DATA_ROOT / "lattice" / "neural_graph.json"
LATTICE_PATH = DATA_ROOT / "lattice" / "department_lattice.json"
LOGS_DIR = DATA_ROOT / "logs"
SECURITY_DIR = DATA_ROOT / "security"

# Workspace roots
WORKSPACE_ROOT = ROOT_DIR / "RealmWorkspaces"
STATIC_DIR = ROOT_DIR / "static"
STATIC_PATH = STATIC_DIR  # Add this line to fix the app.py import error

# Ensure directories exist
LOGS_DIR.mkdir(parents=True, exist_ok=True)
SECURITY_DIR.mkdir(parents=True, exist_ok=True)
(DATA_ROOT / "memory").mkdir(parents=True, exist_ok=True)
(DATA_ROOT / "chroma_db").mkdir(parents=True, exist_ok=True)

# Logging
logger = logging.getLogger("RealmForge")
logger.setLevel(logging.INFO)

fh = logging.FileHandler(LOGS_DIR / "realmforge.log", encoding="utf-8")
fh.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
fh.setFormatter(formatter)
ch.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(fh)
    logger.addHandler(ch)


# ==============================================================================
# Audit Ledger
# ==============================================================================

AUDIT_LEDGER_PATH = DATA_ROOT / "audit" / "contributions.jsonl"
AUDIT_LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)


def log_contribution(agent: str, dept: str, mission_id: str, summary: str) -> None:
    """Appends a contribution record to the audit ledger."""
    record = {
        "agent": agent,
        "department": dept,
        "mission_id": mission_id,
        "summary": summary,
    }
    with open(AUDIT_LEDGER_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
