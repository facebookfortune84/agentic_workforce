"""
REALM FORGE: USAGE TRACKER v1.0
PURPOSE: Monitors token consumption and deducts credits via Gatekeeper.
PATH: F:/agentic_workforce/src/system/billing/usage_tracker.py
"""

from src.auth import gatekeeper
from src.system.config import logger

class UsageTracker:
    @staticmethod
    async def track_llm_usage(response: Any, api_key: str, mission_id: str, agent_id: str, silo: str):
        """
        Extracts usage from LangChain/Groq response and deducts credits.
        """
        # Master Key doesn't pay for electricity
        if api_key == gatekeeper.MASTER_KEY:
            return

        # Extract tokens (Groq/Langchain specific)
        usage = getattr(response, "usage_metadata", {})
        total_tokens = usage.get("total_tokens", 0)
        
        # Calculation: 1 credit per 1000 tokens (Standard Industrial Rate)
        cost = max(1, total_tokens // 1000)

        success = await gatekeeper.deduct_credit(
            api_key=api_key,
            cost=cost,
            mission_id=mission_id,
            agent_id=agent_id,
            silo_id=silo,
            task_context=f"LLM Reasoning ({total_tokens} tokens)"
        )
        
        if success:
            logger.info(f"⚡ [ENERGY] Mission {mission_id}: Deducted {cost} credits for {agent_id}.")
        else:
            logger.warning(f"⚠️ [ENERGY_LOW] Mission {mission_id}: Credit deduction failed.")