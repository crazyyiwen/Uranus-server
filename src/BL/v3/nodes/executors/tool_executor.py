"""Executor for tool nodes (async)."""

import asyncio
from typing import Any, Dict

from BL.v3.nodes.executors.base_executor import BaseNodeExecutor


class ToolNodeExecutor(BaseNodeExecutor):
    """Executor for tool nodes - executes tools/partial views in async mode."""

    async def execute(self, node_config: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute tool node (async). Yields to the event loop so other tasks can run.

        Args:
            node_config: Tool node configuration
            state: Current state

        Returns:
            Tool output
        """
        # Yield to event loop so this coroutine works properly in async context
        await asyncio.sleep(0)

        config = node_config.get("config", {})

        # Resolve tool parameters (CPU-bound; keep fast)
        parameters = config.get("parameters", {})
        resolved_params = {}
        for key, value_template in parameters.items():
            resolved_params[key] = self.variable_resolver.resolve(value_template, state)

        # Tool execution would happen here (use asyncio.to_thread() for blocking calls)
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
