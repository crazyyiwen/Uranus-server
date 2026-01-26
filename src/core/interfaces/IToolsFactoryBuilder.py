

from abc import ABC, abstractmethod


class ToolsBuilder(ABC):

    @abstractmethod
    def build_function_tools(self, path: str):
        """Build agents from agentic workflow JSON file

        Args:
            path: Path to the agentic_workflow.json file

        Returns:
            tools
        """
        pass

    @abstractmethod
    def build_api_tools(self, path: str):
        """Build agents from agentic workflow JSON file

        Args:
            path: Path to the agentic_workflow.json file

        Returns:
            tools
        """
        pass

    @abstractmethod
    def build_view_tools(self, path: str):
        """Build agents from agentic workflow JSON file

        Args:
            path: Path to the agentic_workflow.json file

        Returns:
            tools
        """
        pass




class ToolsFactory(ABC):

    @abstractmethod
    def create_tools_builder(self) -> ToolsBuilder:
        """Create a tools builder instance

        Args:
            self: class itself

        Returns:
            tools builder instance
        """
        pass

    @abstractmethod
    def create_tools_builder_with_mcp(self) -> ToolsBuilder:
        """Create a tools builder instance

        Args:
            self: class itself

        Returns:
            tools builder instance
        """
        pass