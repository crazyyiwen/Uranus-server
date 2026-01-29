"""Executor for workflow nodes - supports recursive composition."""

from typing import Any, Dict

from BL.v3.nodes.executors.base_executor import BaseNodeExecutor


class WorkflowNodeExecutor(BaseNodeExecutor):
    """
    Executor for workflow nodes.

    Workflow nodes can be:
    - Subgraphs (embedded in parent graph)
    - Handoffs (delegation to another workflow)
    - Tools (callable from agents)
    """

    def __init__(self, variable_resolver=None, graph_builder=None):
        """
        Initialize workflow executor.

        Args:
            variable_resolver: Variable resolver instance
            graph_builder: Graph builder for recursive workflow loading
        """
        super().__init__(variable_resolver)
        self.graph_builder = graph_builder

    async def execute(self, node_config: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute workflow node (async).

        Args:
            node_config: Workflow node configuration
            state: Current state

        Returns:
            Workflow output dictionary
        """
        config = node_config.get("config", {})

        # Resolve inputs
        inputs_config = config.get("inputs", {})
        resolved_inputs = self._resolve_inputs(inputs_config, state)

        # Get workflow ID
        workflow_id = config.get("agenticWorkflowId", "")
        if not workflow_id:
            return {
                "output": {"error": "No workflow ID specified"},
                "state": state,
            }

        # If graph_builder is available, invoke the workflow
        if self.graph_builder:
            try:
                # Build workflow node function (returns async LangGraph node function)
                workflow_node_fn = self.graph_builder.build_workflow_node(workflow_id, config)

                # Prepare state for workflow invocation
                workflow_state = {
                    **state,
                    "interface": {
                        "inputs": resolved_inputs,
                    },
                }

                # Invoke workflow node function (async)
                result_state = await workflow_node_fn(workflow_state)

                # Extract relevant output from result
                # Look for output node result or use workflow state
                output_nodes = result_state.get("nodes", {})
                output_result = output_nodes.get("output", {})
                
                output = {
                    "workflowId": workflow_id,
                    "inputs": resolved_inputs,
                    "status": "completed",
                    "messages": result_state.get("messages", []),
                    "result": output_result,
                }
                
                # Update state with workflow result (already merged by node function)
                state = result_state
            except Exception as e:
                output = {
                    "error": str(e),
                    "workflowId": workflow_id,
                    "status": "failed",
                }
        else:
            # No graph builder - return placeholder
            output = {
                "workflowId": workflow_id,
                "inputs": resolved_inputs,
                "status": "pending",
            }

        # Apply variable updates
        updated_state = self._apply_variable_updates(output, node_config, state)

        return {
            "output": output,
            "state": updated_state,
        }

    def get_output_schema(self) -> Dict[str, Any]:
        """Return output schema for workflow node."""
        return {
            "type": "object",
            "properties": {
                "workflowId": {"type": "string"},
                "inputs": {"type": "object"},
                "status": {"type": "string"},
            },
        }
