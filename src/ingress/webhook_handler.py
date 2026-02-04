"""
REALM FORGE: INGRESS HANDLER v1.0
PURPOSE: Receives external signals and converts them into Mission Requests.
PATH: F:/agentic_workforce/src/ingress/webhook_handler.py
"""

from fastapi import APIRouter, Request, Header, HTTPException
from src.system.orchestrator import orchestrator
from src.utils.id_generator import generate_mission_id

router = APIRouter(prefix="/api/v1/ingress", tags=["ingress"])

@router.post("/discord")
async def discord_ingress(request: Request, x_signature: str = Header(None)):
    """Receives triggers from Discord and launches a mission."""
    data = await request.json()
    content = data.get("content", "")
    
    if not content:
        return {"status": "IGNORED", "reason": "Empty payload"}

    # Launch Mission via Orchestrator
    mission_id = generate_mission_id()
    # We trigger the strike in the background
    import asyncio
    asyncio.create_task(orchestrator.execute_multi_agent_strike(
        directive=content,
        user_id=f"DISCORD_USER_{data.get('author', {}).get('id')}"
    ))

    return {"status": "MISSION_IGNITED", "mission_id": mission_id}
