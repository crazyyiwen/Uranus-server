

from BL.agents.build_tools.centralized_agent_tools_service import CentralizedTools
from BL.agents.build_tools.decentralized_agent_tools_service import DecentralizedTools
from core.interfaces.IToolsFactoryBuilder import Tools, ToolsBuilder


class CentralizedAgentToolsBuilder(ToolsBuilder):
    """
    Centralized Agent Tools Builder
    """
    def build_dynamic_tools(self)->Tools:
        """
        
        Build and return the tools for Centralized Agent.
        Returns:
            list: A list of tools for Centralized Agent.
        """
        # Implementation for building Centralized Agent tools goes here
        return CentralizedTools()
    
    def build_dynamic_tools_with_mcp(self)->Tools:
        """
        Build and return the tools for Centralized Agent.
        Returns:
            list: A list of tools for Centralized Agent.
        """
        # Implementation for building Centralized Agent tools goes here
        return DecentralizedTools()
    
class DecentralizedAgentToolsBuilder(ToolsBuilder):
    """
    Decentralized Agent Tools Builder
    """
    def build_dynamic_tools(self)->Tools:
        """
        Build and return the tools for Decentralized Agent.
        Returns:
            list: A list of tools for Decentralized Agent.
        """
        # Implementation for building Decentralized Agent tools goes here
        return DecentralizedTools()
    
    def build_dynamic_tools_with_mcp(self)->Tools:
        """
        Build and return the tools for Decentralized Agent.
        Returns:
            list: A list of tools for Decentralized Agent.
        """
        # Implementation for building Decentralized Agent tools goes here
        pass