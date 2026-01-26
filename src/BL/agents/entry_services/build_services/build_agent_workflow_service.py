import json
from pathlib import Path
from typing import Dict, Any, Optional, List

from langgraph.graph import StateGraph, END
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage, ToolMessage, BaseMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import BaseTool

from BL.agents.entry_services.build_services.build_tools.build_tools_service import (
    build_agent_tool,
    build_partial_view_tool,
    build_ssf_call_tool
)
from BL.agents.states.state import CommonAgentState
from BL.agents.agents_model.model_selection import get_dynamic_model_instance, get_default_model_name


class LangGraphAgentWorkflowBuilder:
    """
    Builds complecated LangGraph agents recursively from agentic_workflow.json
    """

    def __init__(self, workflow: Dict[str, Any]):
        self.workflow = workflow
        self.nodes_by_id = {n["id"]: n for n in workflow["nodes"]}
        self.agent_nodes = {
            n["id"]: n for n in workflow["nodes"] if n["type"] == "agent"
        }
        self.edges = workflow["edges"]

        self._graph_cache = {}

    # ---------- public ----------

    def build_root_agent(self):
        start_edges = [e for e in self.edges if e["source"] == "start"]
        for e in start_edges:
            if e["target"] in self.agent_nodes:
                return self._build_agent_graph(e["target"])
        raise ValueError("No root agent found")

    # ---------- internals ----------

    def _build_agent_graph(self, agent_id: str):
        if agent_id in self._graph_cache:
            return self._graph_cache[agent_id]

        agent_node = self.agent_nodes[agent_id]
        agent_config = agent_node.get("config", {})

        # Extract model configuration
        model_config = agent_config.get("model", {})
        model_code = model_config.get("code", "gpt-4.1")
        model_name = get_default_model_name(model_code)

        # Initialize model
        llm = get_dynamic_model_instance(model_name, temperature=0.0)
        if llm is None:
            # Fallback to default model
            llm = ChatOpenAI(model="gpt-4o", temperature=0)

        # Extract prompt template
        prompt_templates = agent_config.get("promptTemplate", [])
        system_message = self._build_system_message(prompt_templates)

        # Extract max iterations
        max_iterations = agent_config.get("maxIterations", 10)

        # Build tools for this agent
        tools = self._build_tools_for_agent(agent_id)

        # Bind tools to LLM
        llm_with_tools = llm.bind_tools(tools) if tools else llm

        # Build tools map for execution
        tools_by_name = {tool.name: tool for tool in tools}

        # Define agent node function
        def agent_node_fn(state: CommonAgentState):
            """Main agent reasoning node - calls LLM with tools"""
            messages = state.get("messages", [])
            iteration_count = state.get("iteration_count", 0)

            # Add system message if not present
            if not messages or not isinstance(messages[0], SystemMessage):
                messages = [SystemMessage(content=system_message)] + messages

            # Call LLM
            response = llm_with_tools.invoke(messages)

            # Increment iteration count
            iteration_count += 1

            # Return updated state with new message and iteration count
            return {
                "messages": messages + [response],
                "iteration_count": iteration_count
            }

        # Define tool execution node
        def tool_execution_node(state: CommonAgentState):
            """Execute tools requested by the agent"""
            messages = state.get("messages", [])
            last_message = messages[-1] if messages else None

            if not last_message or not hasattr(last_message, "tool_calls"):
                return {"messages": messages}

            tool_calls = last_message.tool_calls or []
            tool_messages = []

            for tool_call in tool_calls:
                tool_name = tool_call.get("name")
                tool_args = tool_call.get("args", {})
                tool_call_id = tool_call.get("id")

                if tool_name in tools_by_name:
                    try:
                        # Execute the tool
                        tool = tools_by_name[tool_name]
                        result = tool.invoke(tool_args)

                        # Create tool message with result
                        tool_messages.append(
                            ToolMessage(
                                content=str(result),
                                tool_call_id=tool_call_id,
                                name=tool_name
                            )
                        )
                    except Exception as e:
                        # Return error message
                        tool_messages.append(
                            ToolMessage(
                                content=f"Error executing {tool_name}: {str(e)}",
                                tool_call_id=tool_call_id,
                                name=tool_name
                            )
                        )
                else:
                    # Tool not found
                    tool_messages.append(
                        ToolMessage(
                            content=f"Tool {tool_name} not found",
                            tool_call_id=tool_call_id,
                            name=tool_name
                        )
                    )

            return {"messages": messages + tool_messages}

        # Define routing function
        def should_continue(state: CommonAgentState):
            """Determine if we should continue to tools or end"""
            messages = state.get("messages", [])
            iteration_count = state.get("iteration_count", 0)
            last_message = messages[-1] if messages else None

            # Check if max iterations reached
            if iteration_count >= max_iterations:
                return "end"

            # If last message has tool calls, continue to tools
            if last_message and hasattr(last_message, "tool_calls") and last_message.tool_calls:
                return "tools"

            # Otherwise, end
            return "end"

        # Build the graph manually using add_node
        graph = StateGraph(CommonAgentState)

        # Add nodes
        graph.add_node("agent", agent_node_fn)
        graph.add_node("tools", tool_execution_node)

        # Set entry point
        graph.set_entry_point("agent")

        # Add conditional edges
        graph.add_conditional_edges(
            "agent",
            should_continue,
            {
                "tools": "tools",
                "end": END
            }
        )

        # After tools, go back to agent
        graph.add_edge("tools", "agent")

        # Compile the graph
        compiled = graph.compile()

        self._graph_cache[agent_id] = compiled
        return compiled

    def _build_system_message(self, prompt_templates: list) -> str:
        """Extract and build system message from prompt templates"""
        system_messages = []
        user_messages = []

        for template in prompt_templates:
            role = template.get("role", "")
            text = template.get("text", "")

            if role == "system":
                system_messages.append(text)
            elif role == "user":
                user_messages.append(text)

        # Combine system messages
        combined_system = "\n\n".join(system_messages) if system_messages else "You are a helpful AI assistant."

        # If there are user message templates, add them as context
        if user_messages:
            combined_system += "\n\nUser context templates:\n" + "\n".join(user_messages)

        return combined_system


    def _build_tools_for_agent(self, agent_id: str):
        agent_node = self.agent_nodes[agent_id]
        tools = []

        for tool_json in agent_node["config"].get("tools", []):
            try:
                name = tool_json.get("name")
                if not name:
                    continue

                description = tool_json.get("description", "")
                meta = tool_json.get("config", {}).get("_meta", {})
                meta_type = meta.get("type")

                # SSF tools
                if meta_type == "ssf-call":
                    tool = build_ssf_call_tool(tool_json)
                    if tool:
                        tools.append(tool)
                    continue

                # Partial views
                if meta_type == "partial-view":
                    tool = build_partial_view_tool(tool_json)
                    if tool:
                        tools.append(tool)
                    continue

                # Agent tools via handoff edges
                tool_id = tool_json.get("_id")
                target_agent_id = self._find_handoff_target(agent_id, tool_id)
                if target_agent_id:
                    # Recursively build the sub-agent
                    subgraph = self._build_agent_graph(target_agent_id)
                    tool = build_agent_tool(name, description, subgraph)
                    if tool:
                        tools.append(tool)

            except Exception as e:
                continue

        return tools

    def _find_handoff_target(self, source_agent_id: str, tool_id: Optional[str]):
        if not tool_id:
            return None

        for e in self.edges:
            if (
                e.get("type") == "handoff"
                and e.get("source") == source_agent_id
                and e.get("data", {}).get("toolId") == tool_id
                and e.get("target") in self.agent_nodes
            ):
                return e.get("target")
        return None
    
def build_langgraph_agents_from_file(path: str):
    workflow = json.loads(Path(path).read_text(encoding="utf-8"))
    builder = LangGraphAgentWorkflowBuilder(workflow)
    return builder.build_root_agent()