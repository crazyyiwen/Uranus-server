"""Executor for start nodes."""

from typing import Any, Dict

from BL.v3.nodes.executors.base_executor import BaseNodeExecutor


class StartNodeExecutor(BaseNodeExecutor):
    """Executor for start nodes - initializes workflow state."""

    async def execute(self, node_config: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute start node - processes variable updates from start config (async).

        Args:
            node_config: Start node configuration
            state: Current state

        Returns:
            Node output dictionary
        """
        # Start node typically just applies variable updates
        output = {"status": "started"}

        # Apply variable updates
        updated_state = self._apply_variable_updates(output, node_config, state)

        return {
            "output": output,
            "state": updated_state,
        }

    def get_output_schema(self) -> Dict[str, Any]:
        """Return output schema for start node."""
        return {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
            },
        }
