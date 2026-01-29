"""Interface for variable resolution and state updates."""

from abc import ABC, abstractmethod
from typing import Any, Dict


class IVariableResolver(ABC):
    """Interface for resolving template variables and updating state."""

    @abstractmethod
    def resolve(self, template: str, state: Dict[str, Any]) -> Any:
        """
        Resolve a template string with state variables.

        Args:
            template: Template string like "{{flow.agentId}}"
            state: Current workflow state

        Returns:
            Resolved value
        """
        pass

    @abstractmethod
    def apply_variable_updates(
        self, updates: list, node_output: Dict[str, Any], state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Apply variable updates to state based on node output.

        Args:
            updates: List of variable update definitions
            node_output: Output from the node
            state: Current state

        Returns:
            Updated state
        """
        pass
