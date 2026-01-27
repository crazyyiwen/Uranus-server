


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