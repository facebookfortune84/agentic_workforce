"""
REALM FORGE: SOVEREIGN VALIDATOR v1.0
PURPOSE: Pre-flight check for 1,100+ agents. Ensures YAML integrity and Tool alignment.
PATH: F:/agentic_workforce/src/orchestration/validator.py
"""

import logging
from pathlib import Path
from src.system.agents.loader import discover_agents
from src.system.arsenal.registry import ALL_TOOLS_LIST
from src.api.schemas.agent_schema import AgentManifest

logger = logging.getLogger("Validator")

def validate_workforce_integrity():
    """Forensic audit of all agents and their assigned tools."""
    agents = discover_agents(force_reload=True)
    arsenal_names = {getattr(t, "name", getattr(t, "tool_name", t.__name__)) for t in ALL_TOOLS_LIST}
    
    report = {
        "total_agents": len(agents),
        "broken_manifests": [],
        "missing_tools": [],
        "status": "NOMINAL"
    }

    for agent in agents:
        name = agent["name"]
        raw_data = agent["raw"]
        
        # 1. Schema Validation
        try:
            AgentManifest(**raw_data)
        except Exception as e:
            report["broken_manifests"].append(f"{name}: Schema Mismatch - {str(e)}")

        # 2. Arsenal Alignment
        assigned_tools = raw_data.get("professional", {}).get("tools_assigned", [])
        for t in assigned_tools:
            if t not in arsenal_names:
                report["missing_tools"].append(f"{name} requires unknown tool: {t}")

    if report["broken_manifests"] or report["missing_tools"]:
        report["status"] = "CRITICAL_ERRORS_FOUND"
        
    return report

if __name__ == "__main__":
    print("🔍 [VALIDATOR] Starting industrial workforce audit...")
    results = validate_workforce_integrity()
    print(f"✅ Audit Complete. Status: {results['status']}")
    if results["missing_tools"]:
        print(f"⚠️ Missing Tools found: {len(results['missing_tools'])}")