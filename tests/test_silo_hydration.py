"""
REALM FORGE: SILO HYDRATION TEST v1.0
PURPOSE: Verifies that agents from all 13 silos load correctly.
PATH: F:/agentic_workforce/tests/test_silo_hydration.py
"""

import pytest
import asyncio
from src.system.agents.factory import AgentFactory
from src.system.agents.loader import discover_agents

@pytest.mark.asyncio
async def test_all_silos_loadable():
    """Confirms that at least one agent can be hydrated from every silo."""
    silos = [
        "Architect", "Data_Intelligence", "Software_Engineering", 
        "DevOps_Infrastructure", "Cybersecurity", "Financial_Ops", 
        "Legal_Compliance", "Research_Development", "Executive_Board", 
        "Marketing_PR", "Human_Capital", "Quality_Assurance", "Facility_Management"
    ]
    
    for silo in silos:
        agent = AgentFactory.create_random_silo_agent(silo)
        assert agent is not None, f"Failed to hydrate agent from silo: {silo}"
        assert agent.department == silo
        print(f"✅ Silo {silo} Hydration: SUCCESS (Agent: {agent.name})")

if __name__ == "__main__":
    # Run simple test manually
    asyncio.run(test_all_silos_loadable())