import os
from pathlib import Path

class AgentFactoryTypes:
    COMMON_REACT = "common_react"
    DEEP_AGENT = "agents"
    
AGENTIC_WORKFLOW_JSON_PATH = Path(__file__).parent.parent.parent.parent / os.path.join("jsons", "agentic_workflow.json")
AGENT_URL = "http://localhost:3316/buying_agent_api/embeddings/search"