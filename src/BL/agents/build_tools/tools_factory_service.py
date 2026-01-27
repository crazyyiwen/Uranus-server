


from BL.agents.build_tools.tools_builder_service import CentralizedAgentToolsBuilder, DecentralizedAgentToolsBuilder
from core.interfaces.IToolsFactoryBuilder import ToolsBuilder, ToolsFactory


class CentralizedAgentToolsFactory(ToolsFactory):
    """
    Factory to create Centralized Agent Tools Builder
    """
    def create_tools_builder(self) -> ToolsBuilder:
        """
        Create a CentralizedAgentToolsBuilder instance.
        Returns:
            ToolsBuilder: An instance of CentralizedAgentToolsBuilder.
        """
        return CentralizedAgentToolsBuilder()

    def create_tools_builder_with_mcp(self) -> ToolsBuilder:
        """
        Create a CentralizedAgentToolsBuilder instance with MCP.
        Returns:
            ToolsBuilder: An instance of CentralizedAgentToolsBuilder.
        """
        pass
    
class DecentralizedAgentToolsFactory(ToolsFactory):
    """
    Factory to create Decentralized Agent Tools Builder
    """
    def create_tools_builder(self) -> ToolsBuilder:
        """
        Create a DecentralizedAgentToolsBuilder instance.
        Returns:
            ToolsBuilder: An instance of DecentralizedAgentToolsBuilder.
        """
        return DecentralizedAgentToolsBuilder()
    
    def create_tools_builder_with_mcp(self) -> ToolsBuilder:
        """
        Create a DecentralizedAgentToolsBuilder instance with MCP.
        Returns:
            ToolsBuilder: An instance of DecentralizedAgentToolsBuilder.
        """
        pass