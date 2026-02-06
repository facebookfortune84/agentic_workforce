"""
Speech-to-Text (STT) Routes
---------------------------

Extracted from server.py (v29.2 INDUSTRIAL ULTIMATE).

Provides:
- /api/v1/stt â†’ Whisper-via-Groq transcription
"""

import os
import time
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from groq import Groq

from src.api.dependencies.security import get_license
from src.system.config import BASE_PATH, logger


router = APIRouter(tags=["stt"])


# ==============================================================================
# 1. SPEECH TO TEXT
# ==============================================================================

@router.post("/stt")
async def speech_to_text(
    file: UploadFile = File(...),
    lic = Depends(get_license)
):
    """
    Converts uploaded audio into text using Groq Whisper-large-v3.
    """

    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        # Save temporary WAV file
        temp_path = BASE_PATH / f"input_temp_{int(time.time())}.wav"

        with open(temp_path, "wb") as buffer:
            buffer.write(await file.read())

        # Perform transcription
        with open(temp_path, "rb") as af:
            transcription = client.audio.transcriptions.create(
                file=(str(temp_path), af.read()),
                model="whisper-large-v3",
                response_format="json"
            )

        # Cleanup
        try:
            os.remove(temp_path)
        except Exception:
            logger.warning(f"âš ï¸ [STT] Temp file cleanup failed: {temp_path}")

        return {
            "text": (transcription or {}).get("text", "")
        }

    except Exception as e:
        logger.error(f"âŒ [STT_FAULT]: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"STT_FAULT: {str(e)}"
        )
