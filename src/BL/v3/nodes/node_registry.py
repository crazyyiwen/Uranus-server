"""Node registry using Registry pattern for node type lookup."""

from typing import Dict, Type

from BL.v3.interfaces.node_executor import INodeExecutor


class NodeRegistry:
    """
    Registry for node executors by node type.

    Allows registration and lookup of node executors without modifying core logic.
    """

    _registry: Dict[str, Type[INodeExecutor]] = {}

    @classmethod
    def register(cls, node_type: str, executor_class: Type[INodeExecutor]) -> None:
        """
        Register a node executor for a node type.

        Args:
            node_type: Node type string (e.g., "agent", "workflow", "rule")
            executor_class: Class implementing INodeExecutor
        """
        cls._registry[node_type] = executor_class

    @classmethod
    def get_executor(cls, node_type: str) -> Type[INodeExecutor]:
        """
        Get executor class for a node type.

        Args:
            node_type: Node type string

        Returns:
            Executor class

        Raises:
            ValueError: If node type not registered
        """
        if node_type not in cls._registry:
            raise ValueError(f"Node type '{node_type}' not registered. Available: {list(cls._registry.keys())}")
        return cls._registry[node_type]

    @classmethod
    def create_executor(cls, node_type: str) -> INodeExecutor:
        """
        Create an instance of executor for a node type.

        Args:
            node_type: Node type string

        Returns:
            Executor instance
        """
        executor_class = cls.get_executor(node_type)
        return executor_class()

    @classmethod
    def is_registered(cls, node_type: str) -> bool:
        """Check if a node type is registered."""
        return node_type in cls._registry
