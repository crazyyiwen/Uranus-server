from pathlib import Path
from typing import Any
from fastapi import Request
from langchain_core.messages import HumanMessage

from BL.agents.entry_services.build_services.build_agents_provider_service import AgentFactoryProvider
from core.constant import AgentFactoryTypes, AGENTIC_WORKFLOW_JSON_PATH


# Build agent from workflow JSON
agent_graph: Any = None
try:
    factory = AgentFactoryProvider.get_factory(AgentFactoryTypes.CENTRALIZED_AGENT)
    builder = factory.create_agent_builder()
    agent_graph = builder.build_dynamic_agents(str(AGENTIC_WORKFLOW_JSON_PATH))
except Exception as e:
    raise e


async def agent_invoke(request: Request):
    """
    Invoke the agent built from agentic_workflow.json

    Request body should contain:
    {
        "query": "User question or message"
    }
    """
    try:
        # Parse request body
        user_input = await request.json()

        if 'query' not in user_input:
            raise ValueError("Missing 'query' in request payload.")

        if agent_graph is None:
            raise ValueError("Agent graph is not properly initialized.")

        query = user_input['query']

        # Invoke the agent graph with proper message format
        result = await agent_graph.ainvoke({
            "messages": [HumanMessage(content=query)],
            "iteration_count": 0
        })

        return result

    except Exception as ex:
        raise ex