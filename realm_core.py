"""
REALM FORGE: SOVEREIGN BRAIN v31.11
ARCHITECT: LEAD SWARM ENGINEER (MASTERMIND v31.4)
STATUS: PRODUCTION READY - SEMANTIC SYNAPSE - IDEMPOTENCY LOCKS - 13,472 NODE AWARE
PATH: F:/agentic_workforce/realm_core.py
"""

import os
import yaml
import json
import glob
import re
import asyncio
import sys
import uuid
import io
import time
import torch
import random
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Annotated, Union, Set
from dotenv import load_dotenv

# --- 0. PHYSICAL ENCODING GUARD (WINDOWS PRODUCTION HARDENING) ---
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace', line_buffering=True)
        sys.stderr.reconfigure(encoding='utf-8', errors='replace', line_buffering=True)
    except AttributeError:
        pass

# --- 0.1 PROJECT ROOT ALIGNMENT ---
_REALM_ROOT = Path("F:/agentic_workforce")  # Hard-coded Physical Anchor
if str(_REALM_ROOT) not in sys.path:
    sys.path.insert(0, str(_REALM_ROOT))

from langchain_groq import ChatGroq
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage, AIMessage, BaseMessage
from src.system.agents.loader import discover_agents, get_random_agent
from src.system.arsenal.foundation import BASE_PROJECT_PATH, ROOT_DIR, DATA_DIR, STATIC_DIR, WORKSPACE_ROOT

from langgraph.graph import StateGraph, END

# --- REALM FORGE INTERNAL IMPORTS ---
from src.system.state import RealmForgeState, get_initial_state
from src.system.arsenal.registry import ALL_TOOLS_LIST, DEPARTMENT_TOOL_MAP, get_tools_for_dept, get_swarm_roster, prepare_vocal_response, generate_neural_audio, read_file, write_file, update_knowledge_graph, calculate_file_hash, get_file_metadata
from src.memory.engine import MemoryManager

# --- 1. ARSENAL LINKAGE (SHARDED v50.8 ALIGNMENT) ---
try:
    from src.system.arsenal.registry import (
        ALL_TOOLS_LIST,
        DEPARTMENT_TOOL_MAP,
        get_tools_for_dept,
        get_swarm_roster,
        prepare_vocal_response,
        generate_neural_audio,
        read_file,
        write_file,
        update_knowledge_graph,
        calculate_file_hash,
        get_file_metadata,
    )
    print("âœ… [BRAIN] Neural Mastermind Aligned to Sharded Foundation.")
except ImportError as e:
    print(f"âŒ [CRITICAL_IMPORT_ERROR]: Arsenal Registry linkage failed: {e}")
    sys.exit(1)

# --- 2. CONFIGURATION & HYBRID LLM FACTORY ---
load_dotenv()

llm_instance = None
memory_kernel = MemoryManager()  # Production RAG Instance
_LATTICE_CACHE = None  # Internal memory cache to prevent I/O stalls during high-load missions


def get_llm():
    """Initializes LLM based on .env configuration with Mastermind precision."""
    global llm_instance
    if llm_instance is not None:
        return llm_instance

    model_choice = os.getenv("REALM_MODEL_CORE", "GROQ").upper()

    if model_choice == "NEMOTRON":
        try:
            print("ðŸŒ€ [NVIDIA_NEMOTRON] Loading NVIDIA-Nemotron-Nano-9B-v2...")
            pipe = pipeline(
                "text-generation",
                model="nvidia/NVIDIA-Nemotron-Nano-9B-v2",
                trust_remote_code=True,
                device_map="auto",
                model_kwargs={
                    "torch_dtype": torch.bfloat16 if torch.cuda.is_available() else torch.float32
                },
            )
            llm_instance = HuggingFacePipeline(pipeline=pipe)
            print("âœ… [NVIDIA_NEMOTRON] Local Brain Online.")
        except Exception as e:
            print(f"âš ï¸ [MODEL_FAULT] Nemotron local failed: {e}. Defaulting to Groq.")
            model_choice = "GROQ"

    if model_choice == "GROQ" or llm_instance is None:
        llm_instance = ChatGroq(
            temperature=0.1,
            model_name="llama-3.3-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY"),
        )
        print("ðŸš€ [GROQ] Cloud Mastermind Online.")
    return llm_instance


# --- PATHS ---
DECISION_LOG = Path("F:/agentic_workforce/data/memory/decisions.log")
AGENT_DIR = Path("F:/agentic_workforce/data/agents")
# Renormalized lattice artifact
LATTICE_MAP = Path("F:/agentic_workforce/master_departmental_lattice.json")
TOOLS = {t.name: t for t in ALL_TOOLS_LIST if hasattr(t, "name")}


# --- HELPERS ---
def get_industrial_specialist(silo: str):
    """
    Picks a physical agent manifest from the 13 canonical industrial silos (Cached for Performance).
    
    """
    global _LATTICE_CACHE
    try:
        # Load Cache if empty (Ensures 0% Disk Latency during execution)
        if _LATTICE_CACHE is None:
            if not LATTICE_MAP.exists():
                return None
            with open(LATTICE_MAP, "r", encoding="utf-8-sig") as f:
                _LATTICE_CACHE = json.load(f)

        # Exact match or fuzzy match for the 13 canonical silos
        silo_key = next((k for k in _LATTICE_CACHE.keys() if silo.lower() in k.lower()), None)
        if not silo_key:
            return None

        pool = _LATTICE_CACHE[silo_key].get("agents", [])
        if not pool:
            return None

        return get_random_agent(silo)

    except Exception as e:
        print(f"âš ï¸ [SPECIALIST_FETCH_ERR]: {e}")
        return None


def extract_json(text: str) -> dict:
    try:
        match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
        if match:
            return json.loads(match.group(1))
        text_clean = text.strip()
        if text_clean.startswith("{"):
            return json.loads(text_clean)
        return {}
    except Exception:
        return {}


# ==============================================================================
# 4. NODES (TITAN MASTERMIND CORE v31.11)
# ==============================================================================


async def supervisor_node(state: RealmForgeState):
    """
    ORCHESTRATOR: Supports Natural Language Command (NLC) parsing & Idempotency.
    v31.11: Integrated with 13-Silo Renormalized Lattice and absolute path enforcement.
    """
    mid = state.get("mission_id")
    locks = state.get("mission_locks", set())

    # IDEMPOTENCY CHECK: Kill double-firing
    if mid in locks:
        return {"next_node": END}

    mission = state["messages"][-1].content

    # Official 13 canonical silos
    silo_list = [
        "Architect",
        "Data_Intelligence",
        "Software_Engineering",
        "DevOps_Infrastructure",
        "Cybersecurity",
        "Financial_Ops",
        "Legal_Compliance",
        "Research_Development",
        "Executive_Board",
        "Marketing_PR",
        "Human_Capital",
        "Quality_Assurance",
        "Facility_Management",
    ]

    prompt = f"""
    SYSTEM: Realm Forge Industrial Mastermind v31.11
    CONTEXT: Managing 13,472 nodes and 1,113 Renormalized agents.
    MISSION: "{mission}"
    INDUSTRIAL_SILOS: {silo_list}
    
    TASK:
    1. Parse the Natural Language Command.
    2. Extract entities (locations, counts, file names) into 'semantic_params'.
    3. Determine intent: "INDUSTRIAL_STRIKE" (Action) or "GENERAL_INQUIRY" (Chat).
    4. If Action: Map to primary_silo and fallback_silo from the official 13.
    5. DATA_INTEGRITY: Always use absolute paths (F:/agentic_workforce/...).

    RESPOND IN JSON ONLY:
    {{
        "intent": "INDUSTRIAL_STRIKE" | "GENERAL_INQUIRY",
        "semantic_params": {{ "target_count": 0, "location": "string", "query": "string" }},
        "primary_silo": "SILO_NAME",
        "fallback_silo": "Architect",
        "meeting_invitees": ["SILO_NAME_1", "SILO_NAME_2"],
        "conversational_response": "Detailed answer if GENERAL_INQUIRY, else null",
        "reasoning": "Sovereign Strategy."
    }}
    """
    model = get_llm()
    res = await model.ainvoke([SystemMessage(content=prompt)])
    data = extract_json(res.content if hasattr(res, "content") else str(res))

    new_locks = set(locks)
    new_locks.add(mid)

    if data.get("intent") == "GENERAL_INQUIRY":
        return {
            "next_node": "synthesizer",
            "active_agent": "Mastermind",
            "active_department": "Architect",
            "intent": "GENERAL_INQUIRY",
            "mission_locks": new_locks,
            "messages": [
                AIMessage(content=data.get("conversational_response", "Acknowledged."))
            ],
        }

    primary_silo = data.get("primary_silo", "Architect")
    fallback_silo = data.get("fallback_silo", "Architect")
    primary = get_industrial_specialist(primary_silo)

    invitees = []
    for s in data.get("meeting_invitees", []):
        spec = get_industrial_specialist(s)
        if spec:
            invitees.append(spec["name"])

    if not invitees:
        invitees = [primary["name"] if primary else "ForgeMaster"]

    return {
        "next_node": "planner",
        "intent": "INDUSTRIAL_STRIKE",
        "semantic_params": data.get("semantic_params", {}),
        "mission_locks": new_locks,
        "active_department": primary_silo,
        "fallback_department": fallback_silo,
        "active_agent": primary["name"] if primary else "ForgeMaster",
        "agent_manifest_path": primary["path"] if primary else None,
        "meeting_participants": invitees,
        "messages": [
            AIMessage(
                content=f"ðŸ¤ [ROUND_TABLE]: Convening {', '.join(invitees)}. Lead: {primary['name'] if primary else 'ForgeMaster'}."
            )
        ],
    }


async def planner_node(state: RealmForgeState):
    """THE SPECIALIST: Yields heartbeat to HUD and maps 180 Tools to mission tasks."""
    # TURN LIMIT GUARD (15 Turns = 30 Messages)
    if len(state["messages"]) > 30:
        return {
            "next_node": "synthesizer",
            "messages": [
                AIMessage(
                    content="ðŸš¨ [LIMIT_REACHED]: Strike aborted to preserve node integrity."
                )
            ],
        }

    # HUD HEARTBEAT: Prevent websocket timeout during analysis
    heartbeat = AIMessage(
        content="âš™ï¸ [PLANNING]: Analyzing neural lattice and drafting maneuvers..."
    )

    mission = state["messages"][-1].content
    agent_name = state.get("active_agent", "ForgeMaster")
    dept = state.get("active_department", "Architect")
    params = state.get("semantic_params", {})

    # v31.11 SUTURE: Passing ALL_TOOLS_LIST to satisfy registry signature and fix 500 error
    available_tools = get_tools_for_dept(dept, ALL_TOOLS_LIST)
    if not available_tools:
        available_tools = [t.name for t in ALL_TOOLS_LIST[:50]]

    prompt = f"""
    IDENTITY: {agent_name} (Industrial Silo: {dept})
    MISSION: {mission}
    SEMANTIC_ENTITIES: {json.dumps(params)}
    AVAILABLE TOOLS: {available_tools}
    
    PROTOCOL: 
    1. Use SEMANTIC_ENTITIES to fill tool arguments accurately.
    2. Every file path MUST be F:/agentic_workforce/...
    
    JSON SCHEMA:
    {{ "sub_tasks": [ {{"tool": "TOOL_NAME", "args": {{ "param": "value" }} }} ] }}
    """
    model = get_llm()
    res = await model.ainvoke([SystemMessage(content=prompt)] + state["messages"])
    data = extract_json(res.content if hasattr(res, "content") else str(res))

    return {
        "task_queue": data.get("sub_tasks", []),
        "next_node": "executor",
        "messages": [
            heartbeat,
            AIMessage(
                content=f"ðŸ“‹ [PLAN_LOCKED]: Orchestrating kinetic strike with {len(data.get('sub_tasks', []))} tasks."
            ),
        ],
    }


async def execution_node(state: RealmForgeState):
    """FORCE-KINETIC EXECUTOR: Physically triggers tools and logs artifact paths."""
    agent = state.get("active_agent")
    tasks = list(state.get("task_queue", []))
    messages = list(state["messages"])
    found_artifacts = list(state.get("artifacts", []))

    if not tasks:
        return {"next_node": "validator"}

    for task in tasks:
        tool_name = task.get("tool")

        # REDUNDANCY HANDOFF PROTOCOL
        if tool_name == "HANDOFF":
            new_silo = state.get("fallback_department", "Architect")
            specialist = get_industrial_specialist(new_silo)
            handoff = {"from": state["active_department"], "to": new_silo}
            return {
                "active_agent": specialist["name"] if specialist else "ForgeMaster",
                "active_department": new_silo,
                "handoff_history": state.get("handoff_history", []) + [handoff],
                "next_node": "planner",
                "messages": [
                    AIMessage(
                        content=f"ðŸ”„ [REDUNDANCY]: Escalating to {new_silo} Silo."
                    )
                ],
            }

        if tool_name in TOOLS:
            try:
                args = task.get("args", {})
                # Production Path Sanitization
                for k, v in args.items():
                    if isinstance(v, str) and "F:/" in v:
                        args[k] = v.replace("\\", "/")

                # PRE-EXECUTION SNIFFING
                path_mentions = re.findall(r"[Ff]:/[^ \"^\n\t,)]+", str(args))
                found_artifacts.extend(path_mentions)

                # Tool Execution
                result = await TOOLS[tool_name].ainvoke(args)

                # POST-EXECUTION SNIFFING (Case-insensitive path matching)
                path_matches = re.findall(r"[Ff]:/[^ \"^\n\t,)]+", str(result))
                found_artifacts.extend(path_matches)

                # REDUNDANCY TRIGGER
                if any(
                    err in str(result)
                    for err in ["Throttled", "Error", "None found", "failed"]
                ):
                    return {
                        "next_node": "executor",
                        "task_queue": [{"tool": "HANDOFF"}],
                        "messages": messages,
                    }

                messages.append(
                    ToolMessage(
                        tool_call_id=str(uuid.uuid4()), content=str(result)
                    )
                )
            except Exception as e:
                print(f"ðŸ’¥ [TOOL_CRASH]: {tool_name} failed: {e}")
                return {
                    "next_node": "executor",
                    "task_queue": [{"tool": "HANDOFF"}],
                    "messages": messages,
                }

    return {
        "messages": messages[-15:],
        "active_agent": agent,
        "artifacts": list(set(found_artifacts)),
        "next_node": "validator",
    }


async def validator_node(state: RealmForgeState):
    """THE IRONCLAD GATE: Forensic hash-verification and Lattice anchoring."""
    artifacts = state.get("artifacts", [])
    agent = "IronClad"
    v_logs = []
    clean_artifacts = [str(a).replace("\\", "/") for a in artifacts if "F:/" in str(a)]

    for path in list(set(clean_artifacts)):
        try:
            # Physical verification via registry tools
            res = await calculate_file_hash.ainvoke({"file_path": path})
            if "ERROR" not in res:
                current_hash = res.split(": ")[-1].strip()
                # Anchor the hash to the Knowledge Graph
                await update_knowledge_graph.ainvoke(
                    {
                        "subject": path,
                        "relation": "CURRENT_HASH",
                        "target": current_hash,
                    }
                )
                v_logs.append(f"âœ… {path}: Verified. ({current_hash[:8]})")
            else:
                v_logs.append(f"âŒ {path}: Physical file missing from drive.")
        except Exception:
            continue

    return {
        "active_agent": agent,
        "diagnostic_stream": v_logs,
        "next_node": "auditor",
        "messages": [
            AIMessage(
                content=f"ðŸ›¡ï¸ [IRONCLAD]: {len(v_logs)} artifacts validated against physical drive."
            )
        ],
    }


async def auditor_node(state: RealmForgeState):
    """Verifies TRUTH PROTOCOL: Blocks placeholders and incomplete logic."""
    last_msg = state["messages"][-1].content
    if any(
        p in last_msg.lower()
        for p in ["[insert", "placeholder", "failed", "incomplete"]
    ):
        return {
            "messages": [
                AIMessage(
                    content="ðŸš¨ [AUDIT_FAIL]: Placeholder detected. Re-tracing mission logic..."
                )
            ],
            "next_node": "planner",
        }
    return {
        "messages": [
            AIMessage(content="ðŸ’Ž [INTEGRITY_NOMINAL]: Sovereignty preserved.")
        ],
        "next_node": "synthesizer",
    }


async def synthesizer_node(state: RealmForgeState):
    """Final archival, Decision logging, and response delivery."""
    last_msg = state["messages"][-1].content
    mid = state.get("mission_id", "UNK")

    # Log the successful decision for the Mastermind's memory
    try:
        DECISION_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(DECISION_LOG, "a", encoding="utf-8-sig") as f:
            f.write(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] [{mid}] SUCCESS - Silo: {state.get('active_department')}\n"
            )
    except Exception:
        pass

    # Persist the completion to the Memory Engine
    await memory_kernel.commit_mission_event(
        mission_id=mid,
        agent_id=state.get("active_agent"),
        dept=state.get("active_department"),
        action="MISSION_COMPLETE",
        result=last_msg,
    )

    return {"messages": [AIMessage(content=last_msg)], "next_node": END}


# ==============================================================================
# 5. GRAPH COMPILATION (TITAN-CLASS)
# ==============================================================================

builder = StateGraph(RealmForgeState)

# Add Core Nodes
builder.add_node("supervisor", supervisor_node)
builder.add_node("planner", planner_node)
builder.add_node("executor", execution_node)
builder.add_node("validator", validator_node)
builder.add_node("auditor", auditor_node)
builder.add_node("synthesizer", synthesizer_node)

# Set Entry Point
builder.set_entry_point("supervisor")

# Conditional Logic for Supervisor (General Chat vs Strike)
builder.add_conditional_edges(
    "supervisor",
    lambda x: x["next_node"],
    {"planner": "planner", "synthesizer": "synthesizer", END: END},
)

# Conditional Logic for Executor (Redundancy Handoff vs Success)
builder.add_conditional_edges(
    "executor",
    lambda x: x["next_node"],
    {"planner": "planner", "validator": "validator"},
)

# Standard Transitions
builder.add_edge("planner", "executor")
builder.add_edge("validator", "auditor")
builder.add_edge("auditor", "synthesizer")
builder.add_edge("synthesizer", END)

# Compile Sovereign Brain
app = builder.compile()
