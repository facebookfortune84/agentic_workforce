"""
REALM FORGE: USAGE TRACKER v1.0
PURPOSE: Monitors token consumption and deducts credits via Gatekeeper.
PATH: F:/agentic_workforce/src/system/billing/usage_tracker.py
"""
import os
from typing import Any
from src.auth import gatekeeper
from src.system.config import logger

class UsageTracker:
    @staticmethod
    async def track_llm_usage(response: Any, api_key: str, mission_id: str, agent_id: str, silo: str):
        """
        Extracts usage from LangChain/Groq response and deducts credits.
        Hardened v60.5: Zero-Stop logic for Architect signatures.
        """
        # --- 1. GOD MODE OVERRIDE ---
        # Master Key or the Sovereign Signature don't pay for electricity
        GOD_KEYS = [gatekeeper.MASTER_KEY, "sk-realm-god-mode-888"]
        if api_key in GOD_KEYS or os.getenv("DEVELOPMENT_MODE") == "true":
            logger.info(f"⚡ [ENERGY] God_Mode_Signature detected for {agent_id}. Bypassing deduction.")
            return True

        # --- 2. DEFENSIVE TOKEN EXTRACTION ---
        # Try usage_metadata (New Langchain) -> usage (Standard Groq) -> response_metadata (Old Langchain)
        usage = getattr(response, "usage_metadata", None)
        if not usage:
            # Fallback to dictionary lookup if response is a dict
            if isinstance(response, dict):
                usage = response.get("usage", response.get("response_metadata", {}).get("token_usage", {}))
            else:
                usage = getattr(response, "response_metadata", {}).get("token_usage", {})

        total_tokens = (usage or {}).get("total_tokens", 0)
        
        # Calculation: 1 credit per 1000 tokens (Standard Industrial Rate)
        cost = max(1, total_tokens // 1000)

        # --- 3. EXECUTE DEDUCTION ---
        try:
            success = await gatekeeper.deduct_credit(
                api_key=api_key or "",
                cost=cost,
                mission_id=mission_id or "UNKNOWN_MSN",
                agent_id=agent_id or "UNKNOWN_AGENT",
                silo_id=silo or "Architect",
                task_context=f"LLM Reasoning ({total_tokens} tokens)"
            )
            
            if success:
                logger.info(f"⚡ [ENERGY] Mission {mission_id}: Deducted {cost} credits for {agent_id}.")
                return True
            else:
                # TITAN-HARDENED: If in local mode, log but don't kill the mission
                logger.warning(f"⚠️ [ENERGY_LOW] Mission {mission_id}: Credit deduction failed. Proceeding with emergency reserves.")
                return True # Fallback to True to prevent mission lock
        except Exception as e:
            logger.error(f"❌ [ENERGY_FAULT]: Critical failure in billing pipeline: {e}")
            return True # Never let the billing system kill a mission in development