import os
from pathlib import Path

class AgentFactoryTypes:
    CENTRALIZED_AGENT = "centralized_agent"
    DECENTRALIZED_AGENT = "decentralized_agent"

class ToolsFactoryTypes:
    CENTRALIZED_AGENT = "centralized_agent"
    DECENTRALIZED_AGENT = "decentralized_agent"
    
AGENTIC_WORKFLOW_JSON_PATH_SIMPLE = Path(__file__).parent / os.path.join("jsons", "agentic_workflow_simple.json")
AGENTIC_WORKFLOW_JSON_PATH_COMPLEX = Path(__file__).parent / os.path.join("jsons", "agentic_workflow_complex.json")