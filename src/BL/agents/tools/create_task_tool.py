"""Task delegation tools for context isolation through sub-agents.

This module provides the core infrastructure for creating and managing sub-agents
with isolated contexts. Sub-agents prevent context clash by operating with clean
context windows containing only their specific task description.
"""

from typing import Annotated, NotRequired
from typing_extensions import TypedDict

from langchain_core.messages import ToolMessage, HumanMessage
from langchain_core.tools import BaseTool, InjectedToolCallId, tool
from langgraph.prebuilt import InjectedState  # updated 1.0
from langchain.agents import create_agent

from langgraph.types import Command

from BL.agents.agents_model.model_selection import get_default_model_name, get_dynamic_model_instance
from BL.agents.tools.buildin_tools import ls, read_file, read_todos, write_file, write_todos
from BL.agents.tools.default_tools import search, think_tool

from ..prompts.context_prompts import TASK_DESCRIPTION_PREFIX
from ..states.state import DeepAgentState


class SubAgent(TypedDict):
    """Configuration for a specialized sub-agent."""

    name: str
    description: str
    prompt: str
    model: str
    tools: NotRequired[list[str]]


def create_task_tool(tools, subagents: list[SubAgent], state_schema):
    """Create a task delegation tool that enables context isolation through sub-agents.

    This function implements the core pattern for spawning specialized sub-agents with
    isolated contexts, preventing context clash and confusion in complex multi-step tasks.

    Args:
        tools: List of available tools that can be assigned to sub-agents
        subagents: List of specialized sub-agent configurations
        model: The language model to use for all agents
        state_schema: The state schema (typically DeepAgentState)

    Returns:
        A 'task' tool that can delegate work to specialized sub-agents
    """
    try:
    # Create agent registry
        agents = {}

        # Build tool name mapping for selective tool assignment
        tools_by_name = {}
        for tool_ in tools:
            if not isinstance(tool_, BaseTool):
                tool_ = tool(tool_)
            tools_by_name[tool_.name] = tool_

        # Create specialized sub-agents based on configurations
        for _agent in subagents:
            if "tools" in _agent:
                # Use specific tools if specified
                _tools = [tools_by_name[t] for t in _agent["tools"]]
            else:
                # Default to all tools
                _tools = tools
            model_name = get_default_model_name(_agent.get("model", ""))
            model = get_dynamic_model_instance(model_name=model_name, temperature=0.0)
            if model is None:
                raise ValueError(f"Failed to initialize model {model_name} for sub-agent {_agent['name']}")
            agents[_agent["name"]] = create_agent(
                model, system_prompt=_agent["prompt"], tools=_tools, state_schema=state_schema
            )

        # Generate description of available sub-agents for the tool description
        other_agents_string = [
            f"- {_agent['name']}: {_agent['description']}" for _agent in subagents
        ]

        @tool(description=TASK_DESCRIPTION_PREFIX.format(other_agents=other_agents_string))
        async def task(
            description: str,
            subagent_type: str,
            state: Annotated[DeepAgentState, InjectedState],
            tool_call_id: Annotated[str, InjectedToolCallId],
        ):
            """Delegate a task to a specialized sub-agent with isolated context.

            This creates a fresh context for the sub-agent containing only the task description,
            preventing context pollution from the parent agent's conversation history.
            """
            # Validate requested agent type exists
            if subagent_type not in agents:
                return f"Error: invoked agent of type {subagent_type}, the only allowed types are {[f'`{k}`' for k in agents]}"

            # Get the requested sub-agent
            sub_agent = agents[subagent_type]

            # Create isolated context with only the task description
            # This is the key to context isolation - no parent history
            state["messages"] = [HumanMessage(content=description)]

            # Execute the sub-agent in isolation
            result = await sub_agent.ainvoke(state)

            # Return results to parent agent via Command state update
            return Command(
                update={
                    "files": result.get("files", {}),  # Merge any file changes
                    "messages": [
                        # Sub-agent result becomes a ToolMessage in parent context
                        ToolMessage(
                            result["messages"][-1].content, tool_call_id=tool_call_id
                        )
                    ],
                }
            )

        return task
    except Exception as e:
        return None

# Get tools
def get_delegation_tools(sub_agents: list[SubAgent]):
    try:
        sub_agent_tools = [search, think_tool]

        # Create task tool to delegate tasks to sub-agents
        task_tool = create_task_tool(
            sub_agent_tools, sub_agents, DeepAgentState
        )
        if task_tool is None:
            raise ValueError("Failed to create task delegation tool.")
        delegation_tools = [task_tool]
        all_tools = sub_agent_tools + delegation_tools  # search available to main agent for trivial cases
        return all_tools
    except Exception as e:
        return []