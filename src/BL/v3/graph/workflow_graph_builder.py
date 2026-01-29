"""Main graph builder for v3 workflow system."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from langgraph.graph import END, StateGraph

from BL.v3.interfaces.graph_builder import IGraphBuilder
from BL.v3.nodes.executors.workflow_executor import WorkflowNodeExecutor
from BL.v3.nodes.node_registry import NodeRegistry
from BL.v3.state.workflow_state import WorkflowState, state_reducer
from BL.v3.utils.rule_evaluator import RuleEvaluator
from BL.v3.utils.variable_resolver import VariableResolver


class WorkflowGraphBuilder(IGraphBuilder):
    """
    Builds LangGraph graphs from JSON workflow definitions.

    Supports:
    - All node types (agent, workflow, rule, output, etc.)
    - Recursive workflow composition
    - Conditional edges (rules)
    - Handoffs
    - Variable updates
    """

    def __init__(self, workflow_loader=None):
        """
        Initialize graph builder.

        Args:
            workflow_loader: Function to load workflow JSON by ID
        """
        self.variable_resolver = VariableResolver()
        self.rule_evaluator = RuleEvaluator(self.variable_resolver)
        self.workflow_loader = workflow_loader or self._default_workflow_loader
        self._workflow_cache: Dict[str, Any] = {}
        self._graph_cache: Dict[str, Any] = {}
        self._build_stack: Set[str] = set()  # Track workflows being built (cycle detection)

    def build(self, workflow_definition: Dict[str, Any]) -> Any:
        """
        Build a LangGraph graph from workflow definition.

        Args:
            workflow_definition: Complete workflow JSON definition

        Returns:
            Compiled LangGraph graph
        """
        workflow_id = workflow_definition.get("agenticWorkflowId", "")
        if workflow_id in self._graph_cache:
            return self._graph_cache[workflow_id]

        # Check for cycles
        if workflow_id in self._build_stack:
            raise ValueError(f"Circular dependency detected: workflow {workflow_id}")

        self._build_stack.add(workflow_id)

        try:
            graph = self._build_graph(workflow_definition)
            compiled = graph.compile()
            self._graph_cache[workflow_id] = compiled
            return compiled
        finally:
            self._build_stack.remove(workflow_id)

    def build_workflow_node(
        self, workflow_id: str, workflow_config: Dict[str, Any]
    ) -> Any:
        """
        Build a workflow node (subgraph/handoff/tool) recursively.

        Args:
            workflow_id: ID of the workflow to load
            workflow_config: Configuration for the workflow node

        Returns:
            LangGraph node or tool representing the workflow
        """
        # Load workflow definition
        workflow_def = self.workflow_loader(workflow_id)
        if not workflow_def:
            raise ValueError(f"Workflow {workflow_id} not found")

        # Build the workflow graph
        workflow_graph = self.build(workflow_def)

        # Return async callable node function
        async def workflow_node_fn(state: WorkflowState) -> WorkflowState:
            """Execute workflow node (async)."""
            # Resolve inputs from config
            inputs_config = workflow_config.get("inputs", {})
            resolved_inputs = {}
            for key, value_template in inputs_config.items():
                resolved_inputs[key] = self.variable_resolver.resolve(value_template, state)

            # Prepare state for workflow
            workflow_state = {
                **state,
                "interface": {
                    "inputs": resolved_inputs,
                },
            }

            # Invoke workflow asynchronously
            result = await workflow_graph.ainvoke(workflow_state)

            # Merge results back
            return state_reducer(state, result)

        return workflow_node_fn

    def _build_graph(self, workflow_definition: Dict[str, Any]) -> StateGraph:
        """Build LangGraph StateGraph from workflow definition."""
        nodes = workflow_definition.get("nodes", [])
        edges = workflow_definition.get("edges", [])

        # Create graph
        graph = StateGraph(WorkflowState, reducer=state_reducer)

        # Index nodes by ID
        nodes_by_id = {node["id"]: node for node in nodes}
        nodes_by_type = {}
        for node in nodes:
            node_type = node.get("type", "")
            if node_type not in nodes_by_type:
                nodes_by_type[node_type] = []
            nodes_by_type[node_type].append(node)

        # Determine which node IDs are targets of handoff edges
        handoff_targets = {
            e.get("target")
            for e in edges
            if e.get("type") == "handoff" and e.get("target")
        }

        # Build node functions for all nodes except start/output
        node_functions = {}
        for node in nodes:
            node_id = node["id"]
            node_type = node.get("type", "")

            # Skip start and output - handled specially
            if node_type in ["start", "output"]:
                continue

            # Workflow nodes: only add to the graph if they represent a handoff target
            # (either targeted by a handoff edge, or explicitly marked as handoff in config)
            if node_type == "workflow":
                wf_cfg = node.get("config", {}) or {}
                is_handoff_workflow = (
                    node_id in handoff_targets
                    or wf_cfg.get("type") == "handoff"
                    or wf_cfg.get("nodeType") == "handoff"
                )
                if not is_handoff_workflow:
                    continue

            # Tool nodes: only add to the graph if they represent a handoff target
            # (either targeted by a handoff edge, or explicitly marked as handoff in config)
            if node_type == "tool":
                tool_cfg = node.get("config", {}) or {}
                is_handoff_tool = (
                    node_id in handoff_targets
                    or tool_cfg.get("type") == "handoff"
                    or tool_cfg.get("toolId") == "tool-handoff"
                )
                if not is_handoff_tool:
                    continue

            # Build node function
            node_fn = self._build_node_function(node, nodes_by_id)
            node_functions[node_id] = node_fn
            graph.add_node(node_id, node_fn)

        # Build edges
        self._build_edges(graph, edges, nodes_by_id, nodes_by_type)

        # Set entry point
        start_nodes = nodes_by_type.get("start", [])
        if start_nodes:
            start_node_id = start_nodes[0]["id"]
            # Find edges from start
            start_edges = [e for e in edges if e.get("source") == start_node_id]
            if start_edges:
                target = start_edges[0].get("target")
                graph.set_entry_point(target)

        return graph

    def _build_node_function(self, node: Dict[str, Any], nodes_by_id: Dict[str, Any]):
        """Build a LangGraph node function for a node."""
        node_id = node["id"]
        node_type = node.get("type", "")

        # Get executor - pass graph_builder for workflow nodes
        if node_type == "workflow":
            executor = WorkflowNodeExecutor(
                variable_resolver=self.variable_resolver,
                graph_builder=self
            )
        else:
            executor = NodeRegistry.create_executor(node_type)

        async def node_fn(state: WorkflowState) -> WorkflowState:
            """Execute node and return updated state (async)."""
            result = await executor.execute(node, state)

            # Extract output and updated state
            node_output = result.get("output", {})
            updated_state = result.get("state", state)

            # Store node output in state
            if "nodes" not in updated_state:
                updated_state["nodes"] = {}
            updated_state["nodes"][node_id] = node_output

            return updated_state

        return node_fn

    def _build_edges(
        self,
        graph: StateGraph,
        edges: List[Dict[str, Any]],
        nodes_by_id: Dict[str, Any],
        nodes_by_type: Dict[str, List[Dict[str, Any]]],
    ) -> None:
        """Build edges in the graph."""
        # Group edges by source (excluding start node edges)
        edges_by_source: Dict[str, List[Dict[str, Any]]] = {}
        for edge in edges:
            source = edge.get("source")
            if source == "start":
                continue  # Start edges handled separately
            if source not in edges_by_source:
                edges_by_source[source] = []
            edges_by_source[source].append(edge)

        # Handle rule nodes first - they need conditional edges
        rule_nodes = nodes_by_type.get("rule", [])
        for rule_node in rule_nodes:
            rule_id = rule_node["id"]
            rule_config = rule_node.get("config", {})
            rules = rule_config.get("rules", [])

            # Find edges from this rule
            rule_edges = [e for e in edges if e.get("source") == rule_id]

            if rule_edges:
                # Build conditional routing function
                def build_rule_router(rules: List[Dict[str, Any]], rule_edges: List[Dict[str, Any]]):
                    def route_fn(state: WorkflowState) -> str:
                        """Route based on rule evaluation."""
                        matched_rule_id = self.rule_evaluator.evaluate_rules(rules, state)

                        # Find edge with matching rule ID
                        for edge in rule_edges:
                            source_handle = edge.get("sourceHandle", "")
                            rule_id_str = matched_rule_id if matched_rule_id.startswith("r-") else f"r-{matched_rule_id}"
                            if rule_id_str in source_handle or matched_rule_id in source_handle:
                                target = edge.get("target")
                                if target == "output" or nodes_by_id.get(target, {}).get("type") == "output":
                                    return END
                                return target

                        # Default/else
                        for edge in rule_edges:
                            source_handle = edge.get("sourceHandle", "")
                            if "else" in source_handle.lower() or "default" in source_handle.lower():
                                target = edge.get("target")
                                if target == "output" or nodes_by_id.get(target, {}).get("type") == "output":
                                    return END
                                return target

                        return END

                    return route_fn

                graph.add_conditional_edges(rule_id, build_rule_router(rules, rule_edges))

        # Handle regular edges (non-rule, non-handoff)
        for source_id, source_edges in edges_by_source.items():
            source_node = nodes_by_id.get(source_id)
            if not source_node:
                continue

            source_type = source_node.get("type", "")

            # Skip if already handled (rule nodes)
            if source_type == "rule":
                continue

            # Handoff edges should be represented in the graph as normal transitions
            handoff_edges = [e for e in source_edges if e.get("type") == "handoff"]
            for edge in handoff_edges:
                target = edge.get("target")
                if not target:
                    continue
                if target == "output" or nodes_by_id.get(target, {}).get("type") == "output":
                    graph.add_edge(source_id, END)
                else:
                    graph.add_edge(source_id, target)

            # Regular edges (non-handoff)
            regular_edges = [e for e in source_edges if e.get("type") != "handoff"]

            if not regular_edges:
                continue

            if len(regular_edges) == 1:
                # Single edge - direct connection
                target = regular_edges[0].get("target")
                target_node = nodes_by_id.get(target, {})
                if target == "output" or target_node.get("type") == "output":
                    graph.add_edge(source_id, END)
                else:
                    graph.add_edge(source_id, target)
            else:
                # Multiple edges - route to first non-rule target, or use conditional
                # Check if any target is a rule node
                rule_targets = [
                    e.get("target")
                    for e in regular_edges
                    if nodes_by_id.get(e.get("target", ""), {}).get("type") == "rule"
                ]

                if rule_targets:
                    # Route to first rule node
                    graph.add_edge(source_id, rule_targets[0])
                else:
                    # Route to first target (could be enhanced with conditional logic)
                    target = regular_edges[0].get("target")
                    if target == "output" or nodes_by_id.get(target, {}).get("type") == "output":
                        graph.add_edge(source_id, END)
                    else:
                        graph.add_edge(source_id, target)

        # Handle output nodes - always go to END
        output_nodes = nodes_by_type.get("output", [])
        for output_node in output_nodes:
            output_id = output_node["id"]
            graph.add_edge(output_id, END)

    def _default_workflow_loader(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Default workflow loader - loads from JSON files."""
        # Try to find workflow JSON file
        json_dir = Path(__file__).parent.parent.parent.parent / "core" / "jsons"

        # Try common filenames
        for filename in [
            f"agentic_workflow_{workflow_id}.json",
            f"{workflow_id}.json",
        ]:
            file_path = json_dir / filename
            if file_path.exists():
                with open(file_path, "r", encoding="utf-8") as f:
                    return json.load(f)

        # Try loading from cache if workflow was already loaded
        if workflow_id in self._workflow_cache:
            return self._workflow_cache[workflow_id]

        return None
