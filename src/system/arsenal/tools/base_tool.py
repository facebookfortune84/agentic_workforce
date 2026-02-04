"""
REALM FORGE: TOOL PROXY v1.0
PURPOSE: Standardizes tool execution with UI telemetry and error handling.
PATH: F:/agentic_workforce/src/system/arsenal/tools/base_tool.py
"""

from typing import Any, Dict
from src.system.connection_manager import manager
from src.system.config import logger

class ToolProxy:
    """
    Wraps LangChain tools to provide industrial telemetry 
    back to the Caffeine-Neon UI.
    """
    
    @staticmethod
    async def execute(tool_func: Any, agent_name: str, **kwargs) -> Any:
        tool_name = getattr(tool_func, "name", tool_func.__name__)
        
        # 1. Notify UI via ConnectionManager
        await manager.broadcast({
            "type": "diagnostic",
            "text": f"ðŸ› ï¸ {agent_name} triggered arsenal tool: {tool_name}",
            "agent": agent_name
        })

        try:
            # 2. Execute (LangChain tools use .ainvoke or .run)
            if hasattr(tool_func, "ainvoke"):
                result = await tool_func.ainvoke(kwargs)
            else:
                result = tool_func(**kwargs)
                
            # 3. Log Success
            logger.info(f"[TOOL_SUCCESS] {tool_name} executed by {agent_name}")
            return result

        except Exception as e:
            logger.error(f"[TOOL_ERROR] {tool_name} failed: {str(e)}")
            return f"[ERROR] Arsenal tool '{tool_name}' failed: {str(e)}"
