"""
REALM FORGE: MISSION ENGINE v1.0
PURPOSE: The execution core that iterates through mission strategies, 
         hydrates specialists, and manages the tool-execution loop.
PATH: F:/agentic_workforce/src/system/missions/mission_engine.py
"""

import logging
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from realm_core import get_llm, extract_json

from src.system.agents.factory import AgentFactory, AgentInstance
from src.system.state import RealmForgeState
from src.memory.engine import MemoryManager

logger = logging.getLogger("MissionEngine")

class MissionEngine:
    def __init__(self):
        self.memory = MemoryManager()
        self.llm = get_llm()

    async def run_mission_step(self, state: RealmForgeState, step_data: Dict[str, Any]) -> RealmForgeState:
        """
        Executes a single step of the mission strategy.
        1. Identifies the Silo.
        2. Hydrates a specialist via the Factory.
        3. Conducts the tool-execution loop.
        """
        silo = step_data.get("silo", "Architect")
        action_description = step_data.get("action", "General Analysis")
        
        # 1. Hydrate Specialist from the Silo
        agent = AgentFactory.create_random_silo_agent(silo)
        if not agent:
            logger.error(f"Silo {silo} failed to provide an agent.")
            return state

        logger.info(f"🤖 [MISSION_STEP] Agent {agent.name} ({agent.role}) deployed to {silo}.")
        
        # 2. Prepare Context (Retrieve relevant memories)
        relevant_memory = await self.memory.recall(action_description, filter_dept=silo)
        
        system_prompt = agent.get_system_prompt()
        user_prompt = (
            f"CURRENT TASK: {action_description}\n"
            f"RELEVANT CONTEXT: {relevant_memory}\n"
            f"MISSION ID: {state['mission_id']}\n"
            f"Execute the task using your assigned tools if necessary."
        )

        # 3. The Execution Loop (Thinking + Action)
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        # Call LLM
        response = await self.llm.ainvoke(messages)
        content = response.content

        # 4. Check for Tool Usage
        # Logic: If the agent decides to use a tool, we look for tool-call patterns 
        # or JSON blocks in the response.
        if "{" in content and "tool" in content:
            tool_call = extract_json(content)
            if tool_call and "tool_name" in tool_call:
                t_name = tool_call["tool_name"]
                t_args = tool_call.get("args", {})
                
                logger.info(f"🛠️ [TOOL_EXEC] {agent.name} calling {t_name} with {t_args}")
                
                # EXECUTE via the Suture (AgentInstance -> Registry)
                result = await agent.run_tool(t_name, **t_args)
                
                # Save result to state
                state["tool_results"][t_name] = result
                
                # Feedback loop: Let the agent see the result
                messages.append(AIMessage(content=content))
                messages.append(HumanMessage(content=f"TOOL_RESULT: {json.dumps(result)}"))
                
                final_response = await self.llm.ainvoke(messages)
                content = final_response.content

        # 5. Commit to Memory & Update State
        await self.memory.commit_mission_event(
            mission_id=state["mission_id"],
            agent_id=agent.id,
            dept=silo,
            action=action_description,
            result=content
        )

        state["messages"].append(AIMessage(content=f"[{agent.name}]: {content}"))
        state["vitals"]["active_sector"] = silo
        
        return state

    async def execute_full_strategy(self, state: RealmForgeState) -> RealmForgeState:
        """
        Iterates through the entire drafted strategy in the state.
        """
        strategy = state.get("mission_strategy", {})
        steps = strategy.get("steps", [])

        if not steps:
            logger.warning("No steps found in mission strategy.")
            return state

        for i, step in enumerate(steps):
            logger.info(f"🚀 [STEP {i+1}/{len(steps)}] Executing {step['silo']} maneuver...")
            state = await self.run_mission_step(state, step)
            
            # Update strategy progress
            state["mission_strategy"]["current_step"] = i + 1

        return state