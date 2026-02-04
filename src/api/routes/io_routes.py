"""
Artifact I/O Routes
-------------------

Extracted from server.py (v29.2 INDUSTRIAL ULTIMATE).

Provides:
- /api/v1/io/read  â†’ read files from PROD or Workspace
- /api/v1/io/write â†’ write files to PROD or Workspace
"""

import os
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from src.api.dependencies.security import get_license
from src.system.config import ROOT_DIR, WORKSPACE_ROOT, logger


router = APIRouter(tags=["io"])


# ==============================================================================
# 1. REQUEST MODELS
# ==============================================================================

class FileReadRequest(BaseModel):
    path: str


class FileSaveRequest(BaseModel):
    path: str
    content: str


# ==============================================================================
# 2. READ ARTIFACT
# ==============================================================================

@router.post("/read")
async def read_artifact(
    req: FileReadRequest,
    lic = Depends(get_license)
):
    """
    Reads a file from either:
    - F:/agentic_workforce
    - F:/RealmWorkspaces

    Performs path sanitization to prevent traversal.
    """

    try:
        # Strip absolute prefixes to avoid traversal
        clean_path = (
            req.path.replace("F:/agentic_workforce/", "")
                    .replace("F:/RealmWorkspaces/", "")
                    .lstrip("/\\")
        )

        # Try PROD first
        target = ROOT_DIR / clean_path

        # Fallback to Workspace
        if not target.exists():
            target = WORKSPACE_ROOT / clean_path

        if target.exists() and target.is_file():
            return {
                "content": target.read_text(encoding="utf-8-sig", errors="replace"),
                "type": target.suffix,
                "path": req.path
            }

        return {"error": f"File {req.path} not located on physical disk."}

    except Exception as e:
        logger.error(f"âŒ [IO_READ_FAULT]: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"IO_READ_FAULT: {str(e)}"
        )


# ==============================================================================
# 3. WRITE ARTIFACT
# ==============================================================================

@router.post("/write")
async def save_artifact(
    req: FileSaveRequest,
    lic = Depends(get_license)
):
    """
    Writes a file to either:
    - F:/agentic_workforce
    - F:/RealmWorkspaces

    Automatically creates parent directories.
    """

    try:
        clean_path = (
            req.path.replace("F:/agentic_workforce/", "")
                    .replace("F:/RealmWorkspaces/", "")
                    .lstrip("/\\")
        )

        target = ROOT_DIR / clean_path

        # Ensure directory exists
        os.makedirs(target.parent, exist_ok=True)

        # Write file
        target.write_text(req.content, encoding="utf-8-sig")

        return {"status": "SUCCESS"}

    except Exception as e:
        logger.error(f"âŒ [IO_WRITE_FAULT]: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Physical Write Error: {str(e)}"
        )
