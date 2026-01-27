


from BL.agents.entry_services.build_services.build_tools.tools_builder_service import CommonReactTools
from core.interfaces.IToolsFactoryBuilder import ToolsBuilder, ToolsFactory


class CommonReactToolsFactory(ToolsFactory):
    """
    Factory to create Common React Tools Builder
    """
    def create_tools_builder(self) -> ToolsBuilder:
        """
        Create a CommonReactToolsBuilder instance.
        Returns:
            ToolsBuilder: An instance of CommonReactToolsBuilder.
        """
        return CommonReactTools()
    
class DeepAgentToolsFactory(ToolsFactory):
    """
    Factory to create Common React Tools Builder
    """
    def create_tools_builder(self) -> ToolsBuilder:
        """
        Create a CommonReactToolsBuilder instance.
        Returns:
            ToolsBuilder: An instance of CommonReactToolsBuilder.
        """
        return DeepAgentTools()