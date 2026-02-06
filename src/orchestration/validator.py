"""
REALM FORGE: SOVEREIGN VALIDATOR v1.1
PURPOSE: Pre-flight check for 1,100+ agents. Ensures YAML integrity and Tool alignment.
PATH: F:/agentic_workforce/src/orchestration/validator.py
"""

import logging
from pathlib import Path
from src.system.agents.loader import discover_agents
from src.system.arsenal.registry import ALL_TOOLS_LIST
from src.api.schemas.agent_schema import AgentManifest

logger = logging.getLogger("Validator")

def get_tool_identity(t) -> str:
    """Safely extracts the identifier from LangChain tools or standard functions."""
    if hasattr(t, "name"): 
        return t.name
    if hasattr(t, "tool_name"): 
        return t.tool_name
    if hasattr(t, "__name__"): 
        return t.__name__
    return str(t)

def validate_workforce_integrity():
    """Forensic audit of all agents and their assigned tools."""
    agents = discover_agents(force_reload=True)
    
    # Hardened name extraction to prevent AttributeError on StructuredTool objects
    arsenal_names = {get_tool_identity(t) for t in ALL_TOOLS_LIST}
    
    report = {
        "total_agents": len(agents),
        "broken_manifests": [],
        "missing_tools": set(), # Use a set to avoid duplicates in the summary
        "status": "NOMINAL"
    }

    for agent in agents:
        name = agent["name"]
        raw_data = agent["raw"]
        
        # 1. Schema Validation (checks keys like backstory, identity, professional)
        try:
            AgentManifest(**raw_data)
        except Exception as e:
            report["broken_manifests"].append(f"{name}: Schema Mismatch - {str(e)}")

        # 2. Arsenal Alignment (checks if tools in YAML exist in registry.py)
        assigned_tools = (raw_data or {}).get("professional", {}).get("tools_assigned", [])
        for t in assigned_tools:
            if t not in arsenal_names:
                report["missing_tools"].add(t)

    # Final Evaluation
    if report["broken_manifests"] or report["missing_tools"]:
        report["status"] = "CRITICAL_ERRORS_FOUND"
        
    return report

if __name__ == "__main__":
    print("\n" + "="*50)
    print("ðŸ” [VALIDATOR] Starting industrial workforce audit...")
    print("="*50)
    
    results = validate_workforce_integrity()
    
    print(f"ðŸ“Š TOTAL AGENTS SCANNED: {results['total_agents']}")
    print(f"ðŸ“¡ ARSENAL CAPACITY:    {len(ALL_TOOLS_LIST)} tools")
    print(f"âœ… FINAL STATUS:        {results['status']}")
    
    if results["broken_manifests"]:
        print(f"\nâŒ BROKEN MANIFESTS ({len(results['broken_manifests'])}):")
        for err in results["broken_manifests"][:10]: # Limit output to first 10
            print(f"   - {err}")

    if results["missing_tools"]:
        print(f"\nâš ï¸  MISSING TOOLS FROM ARSENAL ({len(results['missing_tools'])}):")
        # List the missing tools so you know which ones to add to silo files
        for tool_name in sorted(list(results["missing_tools"]))[:20]: 
            print(f"   - [ ] {tool_name}")
        if len(results["missing_tools"]) > 20:
            print(f"   ... and {len(results['missing_tools']) - 20} others.")

    print("="*50 + "\n")
