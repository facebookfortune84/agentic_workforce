"""
Assistant Chat Routes
---------------------

Extracted from server.py (v29.2 INDUSTRIAL ULTIMATE).

Provides:
- Chat endpoint using Groq LLM
- Memory recall integration
- License validation
"""

import os
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from groq import Groq

from src.api.dependencies.security import get_license
from src.memory.engine import MemoryManager
from src.system.config import logger


router = APIRouter(tags=["assistant"])


# ==============================================================================
# 1. REQUEST MODEL
# ==============================================================================

class ChatRequest(BaseModel):
    message: str


# ==============================================================================
# 2. ASSISTANT CHAT ENDPOINT
# ==============================================================================

@router.post("/chat")
async def assistant_chat(
    req: ChatRequest,
    lic = Depends(get_license)
):
    """
    Chat endpoint for the ForgeMaster Consultant.

    - Recalls memory context
    - Sends prompt to Groq LLM
    - Returns assistant response
    """

    try:
        mem = MemoryManager()

        # Retrieve contextual memory
        context = await mem.recall(req.message, n_results=5)

        groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        res = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": f"You are the ForgeMaster Consultant. Context: {context}"
                },
                {
                    "role": "user",
                    "content": req.message
                }
            ]
        )

        return {
            "response": res.choices[0].message.content
        }

    except Exception as e:
        logger.error(f"âš ï¸ [ASSISTANT_FAULT]: {e}")
        return {
            "response": f"âš ï¸ [ASSISTANT_FAULT]: {str(e)}"
        }
