"""Example usage of the v3 workflow system (sync and async)."""

import asyncio
from pathlib import Path

from BL.v3.workflow_builder import (
    ainvoke_workflow,
    build_initial_state_from_user_input,
    build_workflow_from_file,
    invoke_workflow,
)


def example_basic_workflow():
    """Example of building and invoking a simple workflow (sync)."""
    workflow_file = Path(__file__).parent.parent.parent / "core" / "jsons" / "agentic_workflow_simple.json"
    if not workflow_file.exists():
        print(f"Workflow file not found: {workflow_file}")
        return

    print("Building workflow graph...")
    graph = build_workflow_from_file(str(workflow_file))
    initial_state = build_initial_state_from_user_input("I want to amend a contract")

    print("Invoking workflow (sync)...")
    result = invoke_workflow(graph, initial_state)

    print("\nWorkflow execution completed!")
    print(f"Final messages: {len(result.get('messages', []))}")
    print(f"Flow variables: {result.get('flow', {})}")
    print(f"Node outputs: {list(result.get('nodes', {}).keys())}")


async def example_basic_workflow_async(user_query: str = "I want to amend a contract"):
    """Example of building and invoking a simple workflow (async). Returns result dict."""
    workflow_file = Path(__file__).parent.parent.parent / "core" / "jsons" / "agentic_workflow_simple.json"
    if not workflow_file.exists():
        raise FileNotFoundError(f"Workflow file not found: {workflow_file}")

    graph = build_workflow_from_file(str(workflow_file))
    initial_state = build_initial_state_from_user_input(user_query)
    result = await ainvoke_workflow(graph, initial_state)
    return result

