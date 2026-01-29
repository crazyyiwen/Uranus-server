"""Interface for graph builders."""

from abc import ABC, abstractmethod
from typing import Any, Dict


class IGraphBuilder(ABC):
    """Interface for building LangGraph graphs from JSON definitions."""

    @abstractmethod
    def build(self, workflow_definition: Dict[str, Any]) -> Any:
        """
        Build a LangGraph graph from workflow definition.

        Args:
            workflow_definition: Complete workflow JSON definition

        Returns:
            Compiled LangGraph graph
        """
        pass

    @abstractmethod
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
        pass
