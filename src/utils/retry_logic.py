"""
REALM FORGE: RESILIENCE DECORATORS v1.0
PURPOSE: Handles LLM rate limits and Tool timeouts with UI telemetry.
PATH: F:/agentic_workforce/src/utils/retry_logic.py
"""

import asyncio
import functools
import logging
from typing import Callable, Any
from src.system.connection_manager import manager

logger = logging.getLogger("Resilience")

def industrial_retry(
    retries: int = 3, 
    delay: float = 2.0, 
    backoff: float = 2.0,
    silo_context: str = "General"
):
    """
    Decorator that retries async functions. 
    Broadcasts 'REPAIRING' status to the UI via WebSockets.
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            attempt = 0
            current_delay = delay
            
            while attempt < retries:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    if attempt >= retries:
                        logger.error(f"❌ [CRITICAL_FAULT] {func.__name__} failed after {retries} attempts: {e}")
                        await manager.broadcast({
                            "type": "diagnostic",
                            "text": f"CRITICAL FAULT: {silo_context} operation failed permanently.",
                            "agent": "SYSTEM_KERNEL"
                        })
                        raise e
                    
                    # Notify UI of the retry
                    logger.warning(f"⚠️ [RETRY] {func.__name__} attempt {attempt} failed. Retrying in {current_delay}s...")
                    await manager.broadcast({
                        "type": "diagnostic",
                        "text": f"SYSTEM_REPAIR: {silo_context} hiccup detected. Retrying maneuver (Attempt {attempt})...",
                        "agent": "SYSTEM_KERNEL"
                    })
                    
                    await asyncio.sleep(current_delay)
                    current_delay *= backoff
            
        return wrapper
    return decorator