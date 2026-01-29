# V3 Agent Workflow System

A reusable, extensible backend system for dynamically building and executing AI agent workflows from JSON definitions using Python + LangChain + LangGraph.

## Architecture

The system uses several design patterns:

- **Factory Pattern**: Node creation via `NodeRegistry`
- **Strategy Pattern**: Node execution via `INodeExecutor` implementations
- **Registry Pattern**: Node type lookup via `NodeRegistry`
- **Builder Pattern**: Graph construction via `WorkflowGraphBuilder`

## Structure

```
v3/
├── interfaces/          # Core interfaces (INodeExecutor, IGraphBuilder, etc.)
├── nodes/              # Node executors and registry
│   ├── executors/      # Strategy implementations for each node type
│   └── node_registry.py # Registry for node types
├── state/              # State management
├── utils/              # Utilities (variable resolver, rule evaluator)
├── graph/              # Graph building logic
└── workflow_builder.py  # Main entry point
```

## Supported Node Types

- **start**: Workflow entry point
- **output**: Workflow exit point with output mapping
- **agent**: LLM-based reasoning agent with tools
- **workflow**: Recursive workflow composition (subgraph/handoff/tool)
- **rule**: Conditional routing based on state
- **llm**: Standalone LLM call
- **http request**: HTTP API calls
- **variable update**: State variable updates
- **tool**: Tool/partial view execution

## Usage

### Basic Usage

```python
from BL.v3.workflow_builder import build_workflow_from_file, invoke_workflow

# Build workflow from JSON file
graph = build_workflow_from_file("path/to/workflow.json")

# Invoke workflow
initial_state = {
    "messages": [{"role": "user", "content": "Hello"}],
    "flow": {},
    "system": {"userQuery": "Hello"},
    "nodes": {},
    "toolResults": {},
    "iteration_count": 0,
}

result = invoke_workflow(graph, initial_state)
print(result)
```

### Adding New Node Types

1. Create executor class implementing `INodeExecutor`:

```python
from BL.v3.interfaces.node_executor import INodeExecutor
from BL.v3.nodes.executors.base_executor import BaseNodeExecutor

class MyNodeExecutor(BaseNodeExecutor):
    def execute(self, node_config, state):
        # Your logic here
        output = {"result": "..."}
        updated_state = self._apply_variable_updates(output, node_config, state)
        return {"output": output, "state": updated_state}
```

2. Register in `nodes/register_nodes.py`:

```python
from BL.v3.nodes.node_registry import NodeRegistry
NodeRegistry.register("my-node-type", MyNodeExecutor)
```

## Features

- **Recursive Workflow Composition**: Workflow nodes can contain other workflows
- **Conditional Routing**: Rule nodes enable dynamic routing based on state
- **Variable Resolution**: Template variables like `{{flow.agentId}}` are resolved from state
- **State Management**: Shared execution state with flow/system variables
- **Extensibility**: New node types can be added without modifying core logic

## JSON Structure

Workflows are defined in JSON with:

- `nodes`: Array of node definitions
- `edges`: Array of edge definitions connecting nodes
- `variables`: Variable definitions (flow/system scoped)
- `interface`: Input/output interface definition

See `src/core/jsons/agentic_workflow_simple.json` and `agentic_workflow_complex.json` for examples.
