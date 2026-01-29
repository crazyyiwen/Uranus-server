"""Interface for node executors using Strategy pattern."""

from abc import ABC, abstractmethod
from typing import Any, Dict


class INodeExecutor(ABC):
    """Strategy interface for executing different node types."""

    @abstractmethod
    async def execute(self, node_config: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the node logic and return updated state/output (async).

        Args:
            node_config: Node configuration from JSON
            state: Current workflow state

        Returns:
            Dictionary with node output and updated state
        """
        pass

    @abstractmethod
    def get_output_schema(self) -> Dict[str, Any]:
        """
        Return the schema of this node's output.

        Returns:
            JSON schema describing the output structure
        """
        pass
