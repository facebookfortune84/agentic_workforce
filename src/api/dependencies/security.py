"""
Security & License Validation Dependencies
------------------------------------------

Extracted and refactored from server.py (v29.2 INDUSTRIAL ULTIMATE).

This module provides:
- API key header definition
- get_license() dependency for FastAPI routes
- Master key override
- Gatekeeper validation integration
"""

import os
import time
from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader

from src.auth import gatekeeper


# ==============================================================================
# 1. API KEY HEADER
# ==============================================================================

api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False
)


# ==============================================================================
# 2. LICENSE VALIDATION DEPENDENCY
# ==============================================================================

async def get_license(key: str = Security(api_key_header)):
    """
    Validates a RealmForge API key using the Sovereign Gatekeeper.

    - Supports MASTER override key
    - Returns a gatekeeper.License object
    - Raises HTTPException(403) on failure
    """

    master = os.getenv("REALM_MASTER_KEY", "sk-realm-god-mode-888")

    # MASTER OVERRIDE
    if key == master:
        return gatekeeper.License(
            key="MASTER",
            user_id="ROOT_ARCHITECT",
            tier="GOD",
            credits=999999999,
            created_at=time.time(),
            status="ACTIVE"
        )

    # NORMAL LICENSE VALIDATION
    lic = await gatekeeper.validate_key(key)

    if not lic:
        raise HTTPException(
            status_code=403,
            detail="License Invalid. Neural Handshake Failed."
        )

    return lic
