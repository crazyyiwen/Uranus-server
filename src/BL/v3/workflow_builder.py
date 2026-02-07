"""Main entry point for building workflows from JSON."""

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

from BL.v3.graph.workflow_graph_builder import WorkflowGraphBuilder
from BL.v3.nodes.register_nodes import register_all_nodes  # Ensure nodes are registered

logger = logging.getLogger(__name__)

# Optional: cached graph for demo/single-workflow apps (built on first use)
# (_v3_graph_cache, _v3_workflow_definition) keyed by _v3_graph_file
_v3_graph_cache: Optional[Any] = None
_v3_workflow_definition: Optional[Dict[str, Any]] = None
_v3_graph_file: Optional[str] = None

#region Logging
def _get_graph_log_path() -> Path:
    """Resolve log file path at call time (src/BL/v3/log/log.txt)."""
    return Path(__file__).resolve().parent / "log" / "log.txt"


def _write_graph_log(content: str) -> None:
    """Write content to graph structure log file. Path resolved at write time."""
    log_path = _get_graph_log_path()
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(content)
            f.flush()
        logger.info("Graph structure written to: %s", log_path)
    except Exception as ex:
        logger.warning("Could not write graph structure file %s: %s", log_path, ex)
        # Fallback: write to cwd so we at least get a log
        try:
            fallback = Path.cwd() / "v3_graph_structure.log"
            with open(fallback, "w", encoding="utf-8") as f:
                f.write(f"[Fallback log - primary failed: {ex}]\n\n{content}")
                f.flush()
            logger.info("Graph structure written to fallback: %s", fallback)
        except Exception as ex2:
            logger.warning("Fallback write also failed: %s", ex2)

#endregion

#region Graph Structure Logging 

def _log_graph_structure(compiled_graph: Any, workflow_definition: Dict[str, Any], file_path: str) -> None:
    """Build a readable view of the final graph structure and write to log + file."""
    workflow_id = workflow_definition.get("agenticWorkflowId", "")
    name = workflow_definition.get("name", "") or workflow_definition.get("displayName", "")
    # Map node id -> display name from workflow definition
    node_id_to_name: Dict[str, str] = {}
    for node in workflow_definition.get("nodes", []):
        nid = node.get("id", "")
        node_id_to_name[nid] = node.get("name", nid) or nid
    node_id_to_name["__start__"] = "start"
    node_id_to_name["__end__"] = "end"

    def _display_name(nid: str) -> str:
        return node_id_to_name.get(nid, nid)

    # Build node id -> type for rule detection
    node_id_to_type: Dict[str, str] = {}
    for node in workflow_definition.get("nodes", []):
        node_id_to_type[node.get("id", "")] = node.get("type", "")

    lines = [
        "",
        "========== V3 Workflow Graph Structure ==========",
        f"  File: {file_path}",
        f"  Workflow ID: {workflow_id}",
        f"  Name: {name}",
        "----------------------------------------",
    ]
    try:
        g = compiled_graph.get_graph()
        node_ids = [nid for nid in sorted(g.nodes) if nid not in ("__start__", "__end__")]
        edges_list = getattr(g, "edges", [])
        lines.append("  Nodes:")
        for nid in node_ids:
            lines.append(f"    - {_display_name(nid)}")
        lines.append("  Edges:")
        for e in edges_list:
            # Edge may be LangGraph Edge (object with .source/.target) or dict
            if hasattr(e, "source"):
                src_id = getattr(e, "source", "?")
                tgt_id = getattr(e, "target", "?")
                cond = getattr(e, "conditional", False)
            else:
                src_id = e.get("source", "?") if isinstance(e, dict) else "?"
                tgt_id = e.get("target", "?") if isinstance(e, dict) else "?"
                cond = e.get("conditional", False) if isinstance(e, dict) else False
            src = _display_name(src_id)
            tgt = _display_name(tgt_id)
            cond_str = " (conditional)" if cond else ""
            lines.append(f"    {src} -> {tgt}{cond_str}")

        # Conditional edges (from workflow): rule nodes have multiple targets by branch
        rule_edges_from_workflow = [
            edge for edge in workflow_definition.get("edges", [])
            if node_id_to_type.get(edge.get("source", "")) == "rule"
        ]
        if rule_edges_from_workflow:
            lines.append("  Conditional edges (from workflow):")
            for edge in rule_edges_from_workflow:
                src_id = edge.get("source", "?")
                tgt_id = edge.get("target", "?")
                handle = edge.get("sourceHandle", "") or "default"
                src_name = _display_name(src_id)
                tgt_name = _display_name(tgt_id)
                if tgt_id == "output" or node_id_to_type.get(tgt_id) == "output":
                    tgt_name = "end"
                lines.append(f"    {src_name} --[{handle}]--> {tgt_name}")
        lines.append("==========================================")
    except Exception as ex:
        lines.append(f"  (Could not introspect graph: {ex})")
        lines.append("==========================================")
    content = "\n".join(lines)
    logger.info(content)
    _write_graph_log(content)

#endregion

 
async def build_workflow_from_file(file_path: str) -> tuple:
    """
    Build a workflow graph from a JSON file.

    Args:
        file_path: Path to workflow JSON file

    Returns:
        Tuple of (compiled LangGraph graph, workflow_definition dict)
    """
    # Ensure nodes are registered
    register_all_nodes()

    # Load workflow definition
    path = Path(file_path)
    if not path.exists():
        _write_graph_log(f"Workflow file not found: {file_path}\n")
        raise FileNotFoundError(f"Workflow file not found: {file_path}")

    with open(path, "r", encoding="utf-8") as f:
        workflow_definition = json.load(f)

    # Build graph
    try:
        builder = WorkflowGraphBuilder()
        graph = await builder.build(workflow_definition)
    except Exception as ex:
        _write_graph_log(f"Graph build failed: {ex}\nWorkflow file: {file_path}\n")
        logger.exception("Graph build failed")
        raise

    # Log final graph structure view to logger and log file
    _log_graph_structure(graph, workflow_definition, file_path)

    return graph, workflow_definition


async def ainvoke_workflow(graph: Any, initial_state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
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


async def get_v3_graph_for_file(file_path: str) -> Any:
    """
    Build and cache a single workflow graph by file path (e.g. for demo API).
    Same path returns cached graph. Log file is updated on every call (build or cache hit).

    Args:
        file_path: Path to workflow JSON file

    Returns:
        Compiled LangGraph graph
    """
    global _v3_graph_cache, _v3_workflow_definition, _v3_graph_file
    # Write immediately so we know this path was hit (helps debug empty log)
    _write_graph_log(f"get_v3_graph_for_file called: {file_path}\nLog path: {_get_graph_log_path()}\n")
    if _v3_graph_cache is not None and _v3_graph_file == file_path:
        if _v3_workflow_definition is not None:
            _log_graph_structure(_v3_graph_cache, _v3_workflow_definition, file_path)
        return _v3_graph_cache
    _v3_graph_file = file_path
    graph, workflow_definition = await build_workflow_from_file(file_path)
    _v3_graph_cache = graph
    _v3_workflow_definition = workflow_definition
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
