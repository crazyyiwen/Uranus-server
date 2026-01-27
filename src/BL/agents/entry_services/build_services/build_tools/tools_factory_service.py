


from core.interfaces.IToolsFactoryBuilder import ToolsFactory


class CommonReactToolsFactory(ToolsFactory):
    """
    Factory to create Common React Agent Builder
    """
    def create_agent_builder(self) -> ToolsBuilder:
        """
        Create a CommonReactAgent instance.
        Returns:
            ToolsBuilder: An instance of CommonReactToolsBuilder.
        """
        return CommonReactTools()