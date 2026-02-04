"""
REALM FORGE: MISSION ORCHESTRATOR v1.0
ARCHITECT: LEAD SWARM ENGINEER (MASTERMIND v31.4)
STATUS: PRODUCTION READY - MULTI-AGENT STRIKE COORDINATOR
PATH: F:/agentic_workforce/src/system/orchestrator.py
"""

import os
import json
import uuid
import logging
import asyncio
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

# --- INTERNAL SYSTEM LINKAGE ---
from realm_core import app as brain_graph, get_industrial_specialist, extract_json, get_llm
from src.system.state import get_initial_state, RealmForgeState
from src.memory.engine import MemoryManager
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# --- PHYSICAL ANCHOR ---
ROOT_DIR = Path("F:/agentic_workforce")
LATTICE_PATH = ROOT_DIR / "master_departmental_lattice.json"

logger = logging.getLogger("Orchestrator")


class MissionOrchestrator:
    """
    Sovereign Orchestrator: Coordinates multi-agent strikes across 13 industrial silos.
    Handles 'Meeting Mode' logic and sequential mission drafting.
    """

    def __init__(self):
        self.memory = MemoryManager()
        self.llm = get_llm()

    async def draft_mission_strategy(self, directive: str) -> Dict[str, Any]:
        """
        Translates raw input into a multi-step industrial strategy.
        Identifies required silos for the strike.
        """
        prompt = f"""
        SYSTEM: Realm Forge Strategic Orchestrator
        DIRECTIVE: "{directive}"
        
        TASK: Break this mission into a sequence of steps.
        For each step, assign one of the 13 SILOS:
        [Architect, Data_Intelligence, Software_Engineering, DevOps_Infrastructure, 
         Cybersecurity, Financial_Ops, Legal_Compliance, Research_Development, 
         Executive_Board, Marketing_PR, Human_Capital, Quality_Assurance, Facility_Management]

        RESPOND IN JSON ONLY:
        {{
            "mission_title": "STRIKE-ID",
            "required_silos": ["SILO_1", "SILO_2"],
            "steps": [
                {{"step": 1, "silo": "SILO_NAME", "action": "Descriptive action"}}
            ]
        }}
        """
        res = await self.llm.ainvoke([SystemMessage(content=prompt)])
        return extract_json(res.content)

    async def execute_multi_agent_strike(self, directive: str, user_id: str = "ADMIN"):
        """
        High-Level Entry Point for complex missions.
        Triggers the LangGraph Brain and manages the 'Meeting Mode' context.
        """
        # 1. Initialize State
        state = get_initial_state()
        state["messages"].append(HumanMessage(content=directive))
        state["metadata"]["user_id"] = user_id

        # 2. Draft Strategy
        strategy = await self.draft_mission_strategy(directive)
        state["mission_strategy"] = strategy

        logger.info(
            f"ðŸš€ [ORCHESTRATOR] Strike {state['mission_id']} Initiated: {strategy.get('mission_title')}"
        )

        # 3. Execute through Sovereign Brain (LangGraph)
        final_state = await brain_graph.ainvoke(state)

        # 4. Final Audit
        await self.memory.commit_mission_event(
            mission_id=final_state["mission_id"],
            agent_id="ORCHESTRATOR",
            dept="Architect",
            action="STRIKE_SUMMARY",
            result=f"Completed {len(strategy.get('steps', []))} maneuvers across {len(strategy.get('required_silos', []))} silos.",
        )

        return final_state

    async def convene_round_table(
        self, mission_id: str, silos: List[str], topic: str
    ) -> str:
        """
        MEETING MODE: Simulates a multi-agent discussion to generate billable artifacts.
        """
        meeting_transcript = [f"--- ROUND TABLE: {mission_id} ---"]
        participants = []

        # Fetch actual specialists from the renormalized lattice
        for silo in silos:
            specialist = get_industrial_specialist(silo)
            if specialist:
                participants.append(specialist)

        if not participants:
            return "Meeting aborted: No specialists found in required silos."

        # Simulate discussion
        for p in participants:
            prompt = f"""
            IDENTITY: {p['name']} | ROLE: {p['role']}
            MEETING TOPIC: {topic}
            TRANSCRIPT SO FAR: {' '.join(meeting_transcript)}
            
            Provide your expert industrial input for this mission. 
            Be concise, technical, and focus on your sector's contribution.
            """
            res = await self.llm.ainvoke([SystemMessage(content=prompt)])
            contribution = f"[{p['name']} - {p['role']}]: {res.content}"
            meeting_transcript.append(contribution)

        # Archive the meeting
        meeting_file = ROOT_DIR / "data" / "artifacts" / f"meeting_{mission_id}.txt"
        os.makedirs(meeting_file.parent, exist_ok=True)

        with open(meeting_file, "w", encoding="utf-8") as f:
            f.write("\n\n".join(meeting_transcript))

        return str(meeting_file)


# --- GLOBAL INSTANCE ---
orchestrator = MissionOrchestrator()
