"""Executor for tool nodes."""

from typing import Any, Dict

from BL.v3.nodes.executors.base_executor import BaseNodeExecutor


class ToolNodeExecutor(BaseNodeExecutor):
    """Executor for tool nodes - executes tools/partial views."""

    async def execute(self, node_config: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute tool node (async).

        Args:
            node_config: Tool node configuration
            state: Current state

        Returns:
            Tool output
        """
        config = node_config.get("config", {})

        # Resolve tool parameters
        parameters = config.get("parameters", {})
        resolved_params = {}
        for key, value_template in parameters.items():
            resolved_params[key] = self.variable_resolver.resolve(value_template, state)

        # Tool execution would happen here
        # For now, return resolved parameters as output
        output = {
            "toolId": config.get("toolId", ""),
            "parameters": resolved_params,
            "status": "executed",
        }

        # Apply variable updates
        updated_state = self._apply_variable_updates(output, node_config, state)

        return {
            "output": output,
            "state": updated_state,
        }

    def get_output_schema(self) -> Dict[str, Any]:
        """Return output schema for tool node."""
        return {
            "type": "object",
            "properties": {
                "toolId": {"type": "string"},
                "parameters": {"type": "object"},
            },
        }
