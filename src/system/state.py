"""
REALM FORGE: SOVEREIGN STATE BEDROCK v20.0
ARCHITECT: LEAD SWARM ENGINEER (MASTERMIND v31.4)
STATUS: PRODUCTION READY - IDEMPOTENCY LOCKS - BENTO-GRID TELEMETRY
PATH: F:/agentic_workforce/src/system/state.py
"""

import operator
import uuid
from datetime import datetime
from typing import Annotated, List, Dict, Any, TypedDict, Union, Optional, Set
from langchain_core.messages import BaseMessage

# ==============================================================================
# 0. REDUCER LOGIC (KINETIC STATE SYNCHRONIZATION)
# ==============================================================================

def merge_tasks(existing: List[Dict], new: List[Dict]) -> List[Dict]:
    """Sovereign Task Merger: Ensures the mission backlog is unique and sorted."""
    if not isinstance(existing, list): existing = []
    if not isinstance(new, list): new = []
    
    task_map = {(t or {}).get('id'): t for t in existing if (t or {}).get('id')}
    
    for t in new:
        if not isinstance(t, dict): continue
        tid = (t or {}).get('id') or f"task_{uuid.uuid4().hex[:6]}"
        t['id'] = tid
        
        if tid in task_map:
            task_map[tid] = {**task_map[tid], **t} # Update existing
        else:
            task_map[tid] = t # Append new

    return sorted(
        list(task_map.values()), 
        key=lambda x: ((x or {}).get('status', 'OPEN') != 'OPEN', (x or {}).get('priority', 'MEDIUM'), (x or {}).get('id', ''))
    )

def merge_vitals(existing: Dict, new: Dict) -> Dict:
    """Telemetry Merger: Updates real-time HUD vitals without losing historical keys."""
    if not existing: existing = {}
    if not new: return existing
    return {**existing, **new}

def track_handoffs(existing: List[Dict], new: List[Dict]) -> List[Dict]:
    """Spatial Handoff Reducer: Records the flow of data between the 13 industrial silos."""
    if not existing: existing = []
    if not new: return existing
    clean_new = [h for h in new if isinstance(h, dict) and "from" in h and "to" in h]
    return (existing + clean_new)[-15:] # Expanded to 15 for multi-agent meetings

def buffer_diagnostics(existing: List[str], new: List[str]) -> List[str]:
    """Diagnostic Stream Reducer: Manages the Caffeine-Neon terminal buffer."""
    if not existing: existing = []
    if not new: return existing
    return (existing + new)[-100:] # Expanded buffer for high-speed industrial logs

def merge_genesis_protocol(existing: Dict[str, bool], new: Dict[str, bool]) -> Dict[str, bool]:
    """Genesis-100 Tracker: Monitors initialization of the 13 core silos."""
    if not existing: existing = {}
    if not new: return existing
    return {**existing, **new}

def deduplicate_artifacts(existing: List[str], new: List[str]) -> List[str]:
    """Ensures file paths/hashes in the IronClad registry are unique."""
    return list(set((existing or []) + (new or [])))

# ==============================================================================
# 1. STATE DEFINITION (THE TITAN-INDUSTRIAL SCHEMA)
# ==============================================================================

class RealmForgeState(TypedDict):
    """
    The Global Sovereign State for RealmForge.
    v20.0: Added 'mission_strategy' for Orchestrator planning.
    v20.0: Optimized for 13-Silo Bento Grid UI.
    """
    # --- 1. CORE COMMUNICATION ---
    messages: Annotated[List[BaseMessage], operator.add]
    mission_id: str
    intent: str            # "INDUSTRIAL_STRIKE", "INTEL_RECON", etc.
    semantic_params: Dict[str, Any] # Captured entities from NLC
    mission_strategy: Dict[str, Any] # NEW: Step-by-step orchestrator plan
    
    # --- 2. IDENTITY & ROUTING (The 13 Silos) ---
    next_node: str 
    active_agent: str      
    active_department: str 
    fallback_department: str 
    
    # --- 3. MEETING MODE (The Round Table) ---
    meeting_participants: List[str] 
    handoff_history: Annotated[List[Dict[str, str]], track_handoffs] 
    
    # --- 4. TASK MANAGEMENT ---
    task_queue: Annotated[List[Dict[str, Any]], merge_tasks] 
    genesis_tasks: Annotated[Dict[str, bool], merge_genesis_protocol] 
    
    # --- 5. DATA LATTICE & ARTIFACTS ---
    memory_context: str
    artifacts: Annotated[List[str], deduplicate_artifacts]
    tool_results: Dict[str, Any] # NEW: Results from the 180-tool registry
    
    # --- 6. TELEMETRY & DIAGNOSTICS ---
    vitals: Annotated[Dict[str, Any], merge_vitals]
    diagnostic_stream: Annotated[List[str], buffer_diagnostics]
    mission_locks: Annotated[Set[str], operator.or_] 
    
    # --- 7. METADATA ---
    metadata: Dict[str, Any]

# ==============================================================================
# 2. INITIALIZATION (THE CLEAN SLATE)
# ==============================================================================

def get_initial_state() -> RealmForgeState:
    """
    Titan Factory: Initializes the swarm in production mode.
    Anchors the system to F:/agentic_workforce.
    """
    return {
        "messages": [],
        "mission_id": f"MSN-{uuid.uuid4().hex[:8].upper()}",
        "intent": "INDUSTRIAL_STRIKE",
        "semantic_params": {},
        "mission_strategy": {
            "current_step": 0,
            "total_steps": 0,
            "milestones": []
        },
        "next_node": "supervisor",
        "active_agent": "ForgeMaster",
        "active_department": "Architect", 
        "fallback_department": "Software_Engineering",
        "meeting_participants": ["ForgeMaster"],
        "handoff_history": [],
        "task_queue": [],
        "genesis_tasks": {
            "silo_alignment_verification": True,
            "workforce_audit_init": True,
            "arsenal_180_verification": True,
            "lattice_node_ingestion": True,
            "discord_webhook_sync": True
        },
        "memory_context": "Neural uplink stable. F:/ drive pressurized. Awaiting directive.",
        "artifacts": [],
        "tool_results": {},
        "vitals": {
            "ram": 0.0, 
            "cpu": 0.0, 
            "latency": 0.0, 
            "lattice_nodes": 13472,
            "active_sector": "Architect",
            "silo_distribution": {
                "Architect": 86, "Data_Intelligence": 86, "Software_Engineering": 86,
                "DevOps_Infrastructure": 86, "Cybersecurity": 86, "Financial_Ops": 86,
                "Legal_Compliance": 86, "Research_Development": 86, "Executive_Board": 86,
                "Marketing_PR": 86, "Human_Capital": 86, "Quality_Assurance": 86,
                "Facility_Management": 81
            }
        },
        "diagnostic_stream": [f"[{datetime.now().strftime('%H:%M:%S')}] RE-PRESSURIZATION COMPLETE. LATTICE READY."],
        "mission_locks": set(),
        "metadata": {
            "session_id": str(uuid.uuid4()),
            "start_time": datetime.now().isoformat(),
            "version": "20.0.0",
            "ui_theme": "Caffeine-Neon",
            "root_anchor": "F:/agentic_workforce"
        }
    }
