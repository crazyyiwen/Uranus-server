"""Executor for variable update nodes."""

from typing import Any, Dict

from BL.v3.nodes.executors.base_executor import BaseNodeExecutor


class VariableUpdateNodeExecutor(BaseNodeExecutor):
    """Executor for variable update nodes - updates state variables."""

    async def execute(self, node_config: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute variable update node (async).

        Args:
            node_config: Variable update node configuration
            state: Current state

        Returns:
            Updated state output
        """
        # Variable update nodes primarily apply variable updates
        output = {"status": "updated"}

        # Apply variable updates
        updated_state = self._apply_variable_updates(output, node_config, state)

        return {
            "output": output,
            "state": updated_state,
        }

    def get_output_schema(self) -> Dict[str, Any]:
        """Return output schema for variable update node."""
        return {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
            },
        }
