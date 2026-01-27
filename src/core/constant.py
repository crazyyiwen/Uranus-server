import os
from pathlib import Path

class AgentFactoryTypes:
    CENTRALIZED_AGENT = "centralized_agent"
    DECENTRALIZED_AGENT = "decentralized_agent"

class ToolsFactoryTypes:
    CENTRALIZED_AGENT = "centralized_agent"
    DECENTRALIZED_AGENT = "decentralized_agent"
    
AGENTIC_WORKFLOW_JSON_PATH = Path(__file__).parent / os.path.join("jsons", "agentic_workflow_1.json")