"""
REALM FORGE: AGENT FACTORY v1.0
PURPOSE: Hydrates YAML manifests into live AgentInstance objects with 
         direct tool-binding to the Master Arsenal.
PATH: F:/agentic_workforce/src/system/agents/factory.py
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

from src.system.agents import loader
from src.system.arsenal import registry

@dataclass
class AgentInstance:
    """A live instance of an agent from the 13 silos."""
    id: str
    name: str
    role: str
    department: str
    backstory: str
    tools: List[str]
    metadata: Dict[str, Any]
    
    def get_system_prompt(self) -> str:
        """
        Generates the specialized system prompt for the LLM based 
        on the YAML attributes.
        """
        persona = self.metadata.get("attributes", {})
        comm_style = persona.get("communication_style", "Professional")
        personality = ", ".join(persona.get("personality", []))
        
        prompt = (
            f"You are {self.name}, the {self.role} in the {self.department} department.\n"
            f"Your Backstory: {self.backstory}\n"
            f"Communication Style: {comm_style}\n"
            f"Personality Traits: {personality}\n"
            f"STRICT PROTOCOL: You prefer action over words. Adhere to 'Commit Code' protocol.\n"
            f"You have access to the following tools in your arsenal: {', '.join(self.tools)}"
        )
        
        if self.metadata.get("system_metadata", {}).get("god_mode_enabled"):
            prompt += "\nGOD_MODE is ENABLED. You have full system override permissions."
            
        return prompt

    async def run_tool(self, tool_name: str, **kwargs) -> Any:
        """
        Executes a tool from the agent's specific arsenal.
        Checks if the agent is authorized for the tool before execution.
        """
        if tool_name not in self.tools:
            return f"[SECURITY_ERROR] Agent {self.name} is not authorized to use tool: {tool_name}"
        
        # Pass-through to the Master Arsenal Registry
        return await registry.execute_tool(tool_name, **kwargs)


class AgentFactory:
    """The manufacturing plant for agents."""

    @staticmethod
    def create_agent(agent_name: str) -> Optional[AgentInstance]:
        """
        Locates a YAML by name and hydrates it into an AgentInstance.
        """
        manifest = loader.get_agent_by_name(agent_name)
        if not manifest:
            return None
        
        raw = manifest["raw"]
        
        # Standardizing the YAML structure into the instance
        return AgentInstance(
            id=raw.get("identity", {}).get("employee_id", "GEN-0000"),
            name=manifest["name"],
            role=raw.get("professional", {}).get("role_title", "Specialist"),
            department=manifest["department"],
            backstory=raw.get("attributes", {}).get("backstory", ""),
            tools=manifest["tools"],
            metadata=raw
        )

    @staticmethod
    def create_random_silo_agent(department: str) -> Optional[AgentInstance]:
        """Pulls a random specialist from a specific silo (e.g., 'CYBERSECURITY')."""
        manifest = loader.get_random_agent(department)
        if not manifest:
            return None
        return AgentFactory.create_agent(manifest["name"])