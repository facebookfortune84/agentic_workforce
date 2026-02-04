"""
REALM FORGE: AGENT SCHEMAS v1.0
PURPOSE: Validates the complex YAML manifests from the 13 industrial silos.
PATH: F:/agentic_workforce/src/api/schemas/agent_schema.py
"""

from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional
from datetime import datetime

class AgentAttributes(BaseModel):
    backstory: str
    communication_style: str = "Concise"
    personality: List[str] = []
    deployment_status: str = "ACTIVE"

class AgentIdentity(BaseModel):
    full_name: str
    employee_id: str
    created_at: str
    security_clearance: str = "Level 1"

class AgentProfessional(BaseModel):
    department: str
    functional_role: str
    role_title: str
    skills: List[str] = []
    tools_assigned: List[str] = []

class AgentCompliance(BaseModel):
    employee_id: str
    contract_version: str
    employment_type: str
    legal_jurisdiction: str
    work_authorization: str

class AgentSystemMetadata(BaseModel):
    god_mode_enabled: bool = False
    schema_version: str
    project_root: str

class AgentManifest(BaseModel):
    """The Complete Root Schema for a YAML Agent."""
    attributes: AgentAttributes
    identity: AgentIdentity
    professional: AgentProfessional
    compliance: AgentCompliance
    system_metadata: AgentSystemMetadata