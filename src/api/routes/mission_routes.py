"""
REALM FORGE: MISSION ENGINE ROUTES v30.0
PURPOSE: Handles mission ignition, streaming telemetry, and energy deduction.
PATH: F:/agentic_workforce/src/api/routes/mission_routes.py
"""

from fastapi import APIRouter, Depends, HTTPException
from langchain_core.messages import HumanMessage, AIMessage

from src.api.dependencies.security import get_license
from src.api.schemas.mission_schema import MissionRequest
from src.system.connection_manager import manager
from src.system.config import logger, log_contribution
from src.system.state import get_initial_state
from src.system.billing.usage_tracker import UsageTracker
from src.utils.id_generator import generate_mission_id
from src.system.arsenal.registry import (
    prepare_vocal_response,
    generate_neural_audio,
)

router = APIRouter(tags=["mission"])

@router.post("/mission")
async def mission(req: MissionRequest, lic = Depends(get_license)):
    """
    Ignites a mission, streams telemetry via WebSocket, and tracks energy usage.
    """
    try:
        # 1. Standardized Mission Identity
        mission_id = generate_mission_id()

        # 2. Genesis Engine Lazy Load (Avoids circular imports)
        from realm_core import app as genesis_engine

        # 3. State Initialization
        state = get_initial_state()
        state["messages"] = [HumanMessage(content=req.task)]
        state["mission_id"] = mission_id
        state["metadata"]["user_id"] = lic.user_id
        state["vitals"]["active_sector"] = "Architect"

        processed_msg_hashes = set()

        await manager.broadcast({
            "type": "diagnostic",
            "text": f"ðŸš€ Strike {mission_id} Initialized for {lic.user_id}.",
            "agent": "ORCHESTRATOR",
        })

        # 4. Stream & Execute
        async for output in genesis_engine.astream(state):
            for node_name, node_state in output.items():
                if node_name == "__end__":
                    continue

                agent = node_state.get("active_agent") or node_name.upper()
                dept = node_state.get("active_department", "Architect")
                msgs = node_state.get("messages", [])

                # Telemetry Update
                await manager.broadcast({
                    "type": "node_update",
                    "node": node_name.upper(),
                    "agent": agent,
                    "dept": dept,
                    "handoffs": node_state.get("handoff_history", []),
                })

                # 5. Energy Tracking (Usage Tracker Suture)
                if msgs:
                    last_msg = msgs[-1]
                    if isinstance(last_msg, AIMessage):
                        await UsageTracker.track_llm_usage(
                            response=last_msg,
                            api_key=lic.key,
                            mission_id=mission_id,
                            agent_id=agent,
                            silo=dept
                        )

                # 6. Audio Deduplication Logic
                for msg in (msgs if isinstance(msgs, list) else [msgs]):
                    if hasattr(msg, "content") and msg.content and not isinstance(msg, HumanMessage):
                        m_hash = hash(msg.content)
                        if m_hash in processed_msg_hashes: continue
                        processed_msg_hashes.add(m_hash)
                        
                        if any(x in msg.content for x in ["[PLANNING]", "[STRATEGY]"]): continue

                        vocal = prepare_vocal_response(msg.content)
                        audio_payload = await generate_neural_audio(vocal)

                        await manager.broadcast({
                            "type": "audio_chunk",
                            "text": msg.content,
                            "audio_base64": audio_payload,
                            "agent": agent,
                            "dept": dept,
                        })

        await manager.broadcast({"type": "mission_complete", "mission_id": mission_id})
        return {"status": "SUCCESS", "mission_id": mission_id}

    except Exception as e:
        logger.error(f"ðŸ’¥ [MISSION_FAULT]: {e}")
        await manager.broadcast({"type": "error", "message": str(e)})
        raise HTTPException(status_code=500, detail=str(e))
