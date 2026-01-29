"""Extended workflow state for v3 system."""

from typing import Any, Dict, List, Optional
from typing_extensions import TypedDict


class WorkflowState(TypedDict, total=False):
    """
    Extended state structure supporting:
    - Messages (thread history)
    - Flow variables (workflow-scoped)
    - System variables (system-scoped)
    - Node outputs (per-node results)
    - Tool results (from tool invocations)
    - Iteration tracking
    """

    # Message history
    messages: List[Any]

    # Flow-scoped variables (from variables.flow in JSON)
    flow: Dict[str, Any]

    # System-scoped variables (from variables.system in JSON)
    system: Dict[str, Any]

    # Per-node outputs for reference
    nodes: Dict[str, Dict[str, Any]]

    # Tool execution results
    toolResults: Dict[str, Any]

    # Iteration tracking
    iteration_count: int

    # Additional metadata
    metadata: Dict[str, Any]


def state_reducer(left: WorkflowState, right: WorkflowState) -> WorkflowState:
    """
    Reducer function for merging workflow states.
    Right side takes precedence for most fields, with special handling for lists.

    Args:
        left: Existing state
        right: New state updates

    Returns:
        Merged state
    """
    if left is None:
        return right or {}
    if right is None:
        return left

    merged = {**left}

    # Merge flow variables
    if "flow" in right:
        merged["flow"] = {**(left.get("flow", {})), **right["flow"]}

    # Merge system variables
    if "system" in right:
        merged["system"] = {**(left.get("system", {})), **right["system"]}

    # Merge nodes (right takes precedence)
    if "nodes" in right:
        merged["nodes"] = {**(left.get("nodes", {})), **right["nodes"]}

    # Merge tool results
    if "toolResults" in right:
        merged["toolResults"] = {**(left.get("toolResults", {})), **right["toolResults"]}

    # Messages: extend list (right messages appended)
    if "messages" in right:
        left_messages = left.get("messages", [])
        right_messages = right.get("messages", [])
        merged["messages"] = left_messages + right_messages

    # Other fields: right takes precedence
    for key, value in right.items():
        if key not in ["flow", "system", "nodes", "toolResults", "messages"]:
            merged[key] = value

    return merged
