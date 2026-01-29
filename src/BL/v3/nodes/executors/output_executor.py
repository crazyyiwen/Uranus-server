"""Executor for output nodes."""

from typing import Any, Dict

from BL.v3.nodes.executors.base_executor import BaseNodeExecutor


class OutputNodeExecutor(BaseNodeExecutor):
    """Executor for output nodes - finalizes workflow output."""

    async def execute(self, node_config: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute output node - maps state to final output (async).

        Args:
            node_config: Output node configuration
            state: Current state

        Returns:
            Final output dictionary
        """
        output_mapping = node_config.get("config", {}).get("outputMapping", {})

        output = {}
        for key, mapping in output_mapping.items():
            value_template = mapping.get("value", "")
            output[key] = self.variable_resolver.resolve(value_template, state)

        return {
            "output": output,
            "state": state,
        }

    def get_output_schema(self) -> Dict[str, Any]:
        """Return output schema for output node."""
        return {
            "type": "object",
            "properties": {
                "output": {"type": "object"},
            },
        }
