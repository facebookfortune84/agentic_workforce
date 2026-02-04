"""
REALM FORGE: INDUSTRIAL ID GENERATOR v1.0
PURPOSE: Standardizes UUID and human-readable prefixes for the 13-silo workforce.
PATH: F:/agentic_workforce/src/utils/id_generator.py
"""

import uuid
from datetime import datetime

def generate_mission_id() -> str:
    """Returns a MISSION-ID (e.g., MSN-A7B2C9D1)."""
    return f"MSN-{uuid.uuid4().hex[:8].upper()}"

def generate_employee_id() -> str:
    """Returns a GEN-ID for new autonomous entities."""
    return f"GEN-{uuid.uuid4().hex[:6].upper()}"

def generate_artifact_id(ext: str = "json") -> str:
    """Returns a unique filename for artifacts produced in the lattice."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"ART-{ts}-{uuid.uuid4().hex[:4].upper()}.{ext}"

def generate_session_id() -> str:
    """Returns a unique session ID for UI/Socket telemetry."""
    return f"SES-{uuid.uuid4().hex[:12].upper()}"