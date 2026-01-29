# V3 Workflow System Architecture

## Overview

The V3 system is a production-grade, extensible backend for building and executing AI agent workflows from JSON definitions. It uses LangChain and LangGraph to create dynamic, composable agent graphs.

## Design Patterns

### 1. Factory Pattern
- **Location**: `nodes/node_registry.py`
- **Purpose**: Creates node executors based on node type
- **Usage**: `NodeRegistry.create_executor("agent")` returns an `AgentNodeExecutor` instance

### 2. Strategy Pattern
- **Location**: `interfaces/node_executor.py`, `nodes/executors/*.py`
- **Purpose**: Each node type has its own execution strategy
- **Implementation**: All executors implement `INodeExecutor` interface

### 3. Registry Pattern
- **Location**: `nodes/node_registry.py`
- **Purpose**: Maps node types to executor classes
- **Usage**: `NodeRegistry.register("my-type", MyExecutor)`

### 4. Builder Pattern
- **Location**: `graph/workflow_graph_builder.py`
- **Purpose**: Constructs LangGraph graphs from JSON definitions
- **Features**: Handles recursive composition, conditional routing, state management

## Core Components

### 1. Interfaces (`interfaces/`)

- **INodeExecutor**: Strategy interface for node execution
- **IGraphBuilder**: Interface for graph construction
- **IVariableResolver**: Interface for template resolution
- **IRuleEvaluator**: Interface for rule evaluation

### 2. Node Executors (`nodes/executors/`)

Each node type has a dedicated executor:

- **StartNodeExecutor**: Initializes workflow state
- **OutputNodeExecutor**: Maps state to final output
- **AgentNodeExecutor**: LLM-based reasoning with tools
- **WorkflowNodeExecutor**: Recursive workflow composition
- **RuleNodeExecutor**: Conditional routing evaluation
- **LLMNodeExecutor**: Standalone LLM calls
- **HttpRequestNodeExecutor**: HTTP API calls
- **VariableUpdateNodeExecutor**: State variable updates
- **ToolNodeExecutor**: Tool/partial view execution

### 3. State Management (`state/`)

- **WorkflowState**: TypedDict defining workflow state structure
- **state_reducer**: Function for merging states (LangGraph reducer)

State structure:
```python
{
    "messages": List[Message],      # Conversation history
    "flow": Dict[str, Any],          # Flow-scoped variables
    "system": Dict[str, Any],         # System-scoped variables
    "nodes": Dict[str, Dict],         # Per-node outputs
    "toolResults": Dict[str, Any],    # Tool execution results
    "iteration_count": int,          # Iteration tracking
}
```

### 4. Utilities (`utils/`)

- **VariableResolver**: Resolves templates like `{{flow.agentId}}`
- **RuleEvaluator**: Evaluates conditional rules for routing

### 5. Graph Builder (`graph/`)

- **WorkflowGraphBuilder**: Main graph construction logic
  - Builds LangGraph StateGraph from JSON
  - Handles recursive workflow loading
  - Manages conditional edges (rules)
  - Supports handoffs and subgraphs

## Workflow Execution Flow

1. **Load JSON**: Workflow definition loaded from file or dict
2. **Parse Nodes**: Extract nodes, edges, variables from JSON
3. **Build Graph**: Create LangGraph StateGraph
   - Create node functions for each node
   - Register nodes in graph
   - Build edges (conditional and direct)
4. **Compile**: Compile graph to executable form
5. **Invoke**: Execute graph with initial state
6. **Return**: Final state with outputs

## Recursive Workflow Composition

Workflow nodes support three modes:

1. **Subgraph**: Embedded workflow graph in parent graph
2. **Handoff**: Delegation to another workflow (state passed)
3. **Tool**: Callable tool from agent nodes

Implementation:
- `WorkflowNodeExecutor` loads workflow by ID
- `WorkflowGraphBuilder.build_workflow_node()` creates subgraph
- State is merged using `state_reducer`

## Variable Resolution

Templates are resolved using `VariableResolver`:

- `{{flow.variableName}}` → Flow-scoped variables
- `{{system.variableName}}` → System-scoped variables
- `{{nodes.nodeId.outputField}}` → Node outputs
- `{{nodeOutput.field}}` → Current node output
- `{{interface.inputs.field}}` → Interface inputs

## Conditional Routing

Rule nodes enable conditional routing:

1. Rule node evaluates conditions against state
2. Returns matched rule ID
3. Graph routes to edge with matching `sourceHandle`
4. Default/else rule handles fallback

## Extensibility

### Adding a New Node Type

1. **Create Executor**:
```python
from BL.v3.nodes.executors.base_executor import BaseNodeExecutor

class MyNodeExecutor(BaseNodeExecutor):
    def execute(self, node_config, state):
        # Your logic
        output = {"result": "..."}
        updated_state = self._apply_variable_updates(output, node_config, state)
        return {"output": output, "state": updated_state}
```

2. **Register**:
```python
from BL.v3.nodes.node_registry import NodeRegistry
NodeRegistry.register("my-node-type", MyNodeExecutor)
```

3. **Use in JSON**:
```json
{
    "id": "my-node",
    "type": "my-node-type",
    "config": {...}
}
```

### Adding a New Operator

Extend `RuleEvaluator._evaluate_condition()` or `VariableResolver._evaluate_condition()`.

## Error Handling

- **Cycle Detection**: `_build_stack` prevents infinite recursion
- **Missing Nodes**: Validation ensures all referenced nodes exist
- **Invalid Types**: Registry throws `ValueError` for unregistered types

## Performance Considerations

- **Graph Caching**: Compiled graphs cached by workflow ID
- **Workflow Caching**: Loaded workflows cached to avoid re-parsing
- **State Reducer**: Efficient state merging using reducer pattern

## Testing

See `example_usage.py` for basic usage examples.

## Future Enhancements

- Guardrail node executor
- Enhanced tool binding for agents
- Parallel node execution
- Workflow versioning
- State persistence
- Debugging/monitoring hooks
