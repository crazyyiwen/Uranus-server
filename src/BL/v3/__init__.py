"""V3 Agent Workflow System - Reusable, extensible backend for dynamic agent workflows."""

# Demo tools for agentic_workflow_simple.json (handoff and tool nodes)
from BL.v3.demo_tools_v3 import (
    DEMO_LOGS,
    DEMO_TOOLS_REGISTRY,
    call_demo_tool,
    get_demo_logs,
    get_demo_tool,
    was_tool_called,
)

__all__ = [
    "DEMO_LOGS",
    "DEMO_TOOLS_REGISTRY",
    "call_demo_tool",
    "get_demo_logs",
    "get_demo_tool",
    "was_tool_called",
]
