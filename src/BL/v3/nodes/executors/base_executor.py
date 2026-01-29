"""Base executor with common functionality."""

from typing import Any, Dict

from BL.v3.interfaces.node_executor import INodeExecutor
from BL.v3.utils.variable_resolver import VariableResolver


class BaseNodeExecutor(INodeExecutor):
    """Base class for node executors with common functionality."""

    def __init__(self, variable_resolver: VariableResolver = None):
        """
        Initialize base executor.

        Args:
            variable_resolver: Variable resolver instance
        """
        self.variable_resolver = variable_resolver or VariableResolver()

    async def execute(self, node_config: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Base execute implementation. Subclasses should override (async).

        Args:
            node_config: Node configuration
            state: Current state

        Returns:
            Node output dictionary
        """
        raise NotImplementedError("Subclasses must implement execute")

    def get_output_schema(self) -> Dict[str, Any]:
        """
        Default output schema. Subclasses can override.

        Returns:
            JSON schema for output
        """
        return {
            "type": "object",
            "properties": {
                "output": {"type": "string"},
            },
        }

    def _resolve_inputs(self, inputs_config: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Resolve input templates to actual values.

        Args:
            inputs_config: Input configuration with templates
            state: Current state

        Returns:
            Resolved inputs dictionary
        """
        resolved = {}
        for key, value_template in inputs_config.items():
            resolved[key] = self.variable_resolver.resolve(value_template, state)
        return resolved

    def _apply_variable_updates(
        self, node_output: Dict[str, Any], node_config: Dict[str, Any], state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Apply variable updates from node configuration.

        Args:
            node_output: Node execution output
            node_config: Node configuration
            state: Current state

        Returns:
            Updated state
        """
        updates = node_config.get("variableUpdates", [])
        return self.variable_resolver.apply_variable_updates(updates, node_output, state)
