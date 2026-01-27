from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional

from langchain_core.tools import StructuredTool



    
class ToolsBuilder(ABC):

    """
    Centralized Agent Tools Builder
    """
    @abstractmethod
    def build_dynamic_tools(self) -> Tools:
        """
        
        Build and return the tools for Centralized Agent.
        Returns:
            list: A list of tools for Centralized Agent.
        """
    @abstractmethod
    def build_dynamic_tools_with_mcp(self)->Tools:
        """
        Build and return the tools for Centralized Agent.
        Returns:
            list: A list of tools for Centralized Agent.
        """
        # Implementation for building Centralized Agent tools goes here
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

class Tools(ABC):
    @staticmethod
    @abstractmethod
    def _map_json_type_to_python(json_type: str) -> type:
        """Map JSON schema types to Python types"""
        pass

    @staticmethod
    @abstractmethod
    def _create_dynamic_schema(name: str, properties: Dict[str, Any], required: list) -> type:
        """
        Create a dynamic Pydantic model from JSON schema properties.

        Args:
            name: Name for the schema
            properties: JSON schema properties
            required: List of required field names

        Returns:
            Dynamically created Pydantic model
        """
        pass

    @staticmethod
    @abstractmethod
    def _load_executor(executor_config: Dict[str, Any]) -> Optional[Callable]:
        """
        Dynamically load an executor function based on configuration.

        Configuration format:
        {
            "module": "path.to.module",           # Python module path
            "function": "function_name",           # Function to call
            "wrapper": "optional_wrapper_arg"      # Optional argument to pass
        }

        Args:
            executor_config: Executor configuration from JSON

        Returns:
            Callable function or None if loading fails
        """
        pass

    @staticmethod
    @abstractmethod
    def build_ssf_call_tool(tool_config: Dict[str, Any]) -> Optional[StructuredTool]:
        """
        Build a server-side function (SSF) tool dynamically from configuration.

        The tool behavior is completely defined by the JSON configuration.
        No hardcoding - all execution logic is loaded dynamically.

        Configuration structure in _meta:
        {
            "functionId": "...",               # Function identifier
            "moduleId": "...",                 # Module identifier
            "type": "ssf-call",                # Tool type
            "executor": {                      # Optional: custom executor
                "module": "BL.module.path",    # Module to import
                "function": "executor_function", # Function to call
                "wrapper": "wrapper_arg"        # Optional: wrapper argument
            }
        }

        Args:
            tool_config: Complete tool configuration from JSON

        Returns:
            StructuredTool or None if build fails
        """
        pass

    @staticmethod
    @abstractmethod
    def build_partial_view_tool(tool_config: Dict[str, Any]) -> Optional[StructuredTool]:
        """
        Build a partial view rendering tool dynamically from configuration.

        Configuration structure in _meta:
        {
            "type": "partial-view",
            "uiView": "{...}",                 # JSON string of UI configuration
            "executor": {                       # Optional: custom renderer
                "module": "path.to.renderer",
                "function": "render_function"
            }
        }

        Args:
            tool_config: Complete tool configuration from JSON

        Returns:
            StructuredTool or None if build fails
        """
        pass
        
    @staticmethod
    @abstractmethod
    def build_agent_tool(name: str, description: str, agent_graph) -> Optional[StructuredTool]:
        pass
