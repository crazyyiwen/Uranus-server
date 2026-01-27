


from core.constant import ToolsFactoryTypes


class ToolsFactoryProvider:
    """
    Provider to get the appropriate Agent Factory based on type
    """
    @staticmethod
    def get_factory(factory_type: str) -> ToolsFactory:
        """
        Get the appropriate Agent Factory based on the provided type.
        Args:
            factory_type (str): The type of agent factory to retrieve.
            Returns:
            AgentFactory: An instance of the requested Agent Factory."""
        if factory_type == ToolsFactoryTypes.COMMON_REACT:
            pass
        elif factory_type == ToolsFactoryTypes.DEEP_AGENT:
            # return DeepAgentFactory()  # Commented out - deep_agent modules removed
            pass
        else:
            raise ValueError(f"Unsupported factory type: {factory_type}")