"""
REALM FORGE: AGENT LOADER v7.0
PURPOSE: Auto-discovers YAML agent manifests, validates them, and aligns them with
         the 13-silo industrial architecture and the 180-tool arsenal.
PATH: F:/agentic_workforce/src/system/agents/loader.py
"""

import os
import yaml
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

from src.system.arsenal.registry import ALL_TOOLS_LIST
from src.system.arsenal.foundation import DEPARTMENT_TOOL_MAP

AGENT_ROOT = Path("F:/agentic_workforce/data/agents")

# Cache to avoid repeated disk reads
_AGENT_CACHE: Optional[List[Dict[str, Any]]] = None


def _load_yaml(path: Path) -> Optional[Dict[str, Any]]:
    """Safely loads a YAML file with UTF-8 fallback."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception:
        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                return yaml.safe_load(f)
        except Exception:
            return None


def _normalize_department(name: str) -> str:
    """Normalizes department names to match DEPARTMENT_TOOL_MAP keys."""
    if not name:
        return "Architect"

    name_clean = name.strip().replace(" ", "_").upper()

    for dept in DEPARTMENT_TOOL_MAP.keys():
        if name_clean == dept.upper().replace(" ", "_"):
            return dept

    return "Architect"


def _attach_tools(agent_yaml: Dict[str, Any], department: str) -> List[str]:
    """Assigns tools based on department, with YAML overrides."""
    default_tools = (DEPARTMENT_TOOL_MAP or {}).get(department, [])
    override_tools = (agent_yaml or {}).get("professional", {}).get("tools_assigned", [])

    # If YAML specifies tools, merge them with defaults
    merged = list(set(default_tools + override_tools))

    # Filter to ensure tools actually exist in the arsenal
    arsenal_names = {t.name for t in ALL_TOOLS_LIST}
    return [t for t in merged if t in arsenal_names]


def discover_agents(force_reload: bool = False) -> List[Dict[str, Any]]:
    """Discovers all YAML agents across the 13 silos."""
    global _AGENT_CACHE

    if _AGENT_CACHE is not None and not force_reload:
        return _AGENT_CACHE

    agents = []

    for yaml_file in AGENT_ROOT.rglob("*.yaml"):
        data = _load_yaml(yaml_file)
        if not data:
            continue

        # Extract department
        dept = (data or {}).get("professional", {}).get("department", "Architect")
        dept_norm = _normalize_department(dept)

        # Attach tools
        tools = _attach_tools(data, dept_norm)

        # Build agent manifest
        agent_manifest = {
            "name": (data or {}).get("identity", {}).get("full_name", yaml_file.stem),
            "path": str(yaml_file),
            "department": dept_norm,
            "tools": tools,
            "raw": data,
        }

        agents.append(agent_manifest)

    _AGENT_CACHE = agents
    return agents


def get_agents_by_department(dept: str) -> List[Dict[str, Any]]:
    """Returns all agents belonging to a specific silo."""
    dept_norm = _normalize_department(dept)
    return [a for a in discover_agents() if a["department"] == dept_norm]


def get_agent_by_name(name: str) -> Optional[Dict[str, Any]]:
    """Returns a single agent manifest by name."""
    for agent in discover_agents():
        if agent["name"].lower() == name.lower():
            return agent
    return None


def get_random_agent(dept: str) -> Optional[Dict[str, Any]]:
    """Returns a random agent from a department."""
    import random

    pool = get_agents_by_department(dept)
    return random.choice(pool) if pool else None
