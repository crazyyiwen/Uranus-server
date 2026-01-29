"""Main entry point for building workflows from JSON."""

import json
from pathlib import Path
from typing import Any, Dict, Optional

from BL.v3.graph.workflow_graph_builder import WorkflowGraphBuilder
from BL.v3.nodes.register_nodes import register_all_nodes  # Ensure nodes are registered

# Optional: cached graph for demo/single-workflow apps (built on first use)
_v3_graph_cache: Optional[Any] = None
_v3_graph_file: Optional[str] = None


def build_workflow_from_file(file_path: str) -> Any:
    """
    Build a workflow graph from a JSON file.

    Args:
        file_path: Path to workflow JSON file

    Returns:
        Compiled LangGraph graph
    """
    # Ensure nodes are registered
    register_all_nodes()

    # Load workflow definition
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Workflow file not found: {file_path}")

    with open(path, "r", encoding="utf-8") as f:
        workflow_definition = json.load(f)

    # Build graph
    builder = WorkflowGraphBuilder()
    graph = builder.build(workflow_definition)

    return graph


def build_workflow_from_json(workflow_definition: Dict[str, Any]) -> Any:
    """
    Build a workflow graph from a JSON dictionary.

    Args:
        workflow_definition: Workflow definition dictionary

    Returns:
        Compiled LangGraph graph
    """
    # Ensure nodes are registered
    register_all_nodes()

    # Build graph
    builder = WorkflowGraphBuilder()
    graph = builder.build(workflow_definition)

    return graph


def invoke_workflow(graph: Any, initial_state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Invoke a workflow graph with initial state (sync).

    Args:
        graph: Compiled LangGraph graph
        initial_state: Initial state dictionary

    Returns:
        Final state after workflow execution
    """
    if initial_state is None:
        initial_state = _default_initial_state()

    result = graph.invoke(initial_state)
    return result


async def ainvoke_workflow(
    graph: Any, initial_state: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Invoke a workflow graph with initial state (async).

    Args:
        graph: Compiled LangGraph graph
        initial_state: Initial state dictionary

    Returns:
        Final state after workflow execution
    """
    if initial_state is None:
        initial_state = _default_initial_state()

    result = await graph.ainvoke(initial_state)
    return result


def _default_initial_state() -> Dict[str, Any]:
    """Return default initial state for workflow invocation."""
    return {
        "messages": [],
        "flow": {},
        "system": {},
        "nodes": {},
        "toolResults": {},
        "iteration_count": 0,
    }


def get_v3_graph_for_file(file_path: str) -> Any:
    """
    Build and cache a single workflow graph by file path (e.g. for demo API).
    Same path returns cached graph.

    Args:
        file_path: Path to workflow JSON file

    Returns:
        Compiled LangGraph graph
    """
    global _v3_graph_cache, _v3_graph_file
    if _v3_graph_cache is not None and _v3_graph_file == file_path:
        return _v3_graph_cache
    _v3_graph_file = file_path
    _v3_graph_cache = build_workflow_from_file(file_path)
    return _v3_graph_cache


def build_initial_state_from_user_input(user_query: str, **kwargs: Any) -> Dict[str, Any]:
    """
    Build initial workflow state from user input (e.g. from API body).

    Args:
        user_query: User message/query string
        **kwargs: Optional overrides (e.g. flow, system, attachments, interface_inputs)

    Returns:
        Initial state dict for invoke_workflow / ainvoke_workflow
    """
    state = _default_initial_state()
    state["flow"] = {
        "agentId": "",
        "selectedAgentId": "",
        "currentAgentName": "",
        "isPvRendered": False,
        "partialViewData": [],
        **(kwargs.get("flow") or {}),
    }
    state["system"] = {
        "userQuery": user_query,
        "attachments": kwargs.get("attachments") or [],
        **(kwargs.get("system") or {}),
    }
    state["interface"] = {
        "inputs": {
            "message": user_query,
            **(kwargs.get("interface_inputs") or {}),
        },
    }
    state["messages"] = [{"role": "user", "content": user_query}]
    return state
