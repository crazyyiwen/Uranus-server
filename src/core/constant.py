import os
from pathlib import Path

class AgentFactoryTypes:
    COMMON_REACT = "common_react"
    DEEP_AGENT = "agents"

class ToolsFactoryTypes:
    COMMON_REACT = "common_react"
    DEEP_AGENT = "agents"
    
AGENTIC_WORKFLOW_JSON_PATH = Path(__file__).parent / os.path.join("jsons", "agentic_workflow.json")