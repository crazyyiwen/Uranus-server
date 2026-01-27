


from BL.agents.entry_services.build_services.build_tools.tools_factory_service import CommonReactToolsFactory
from core.constant import ToolsFactoryTypes
from core.interfaces.IToolsFactoryBuilder import ToolsFactory


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
            ToolsFactory: An instance of the requested ToolsFactory."""
        if factory_type == ToolsFactoryTypes.COMMON_REACT:
            return CommonReactToolsFactory()
        elif factory_type == ToolsFactoryTypes.DEEP_AGENT:
            pass
        else:
            raise ValueError(f"Unsupported factory type: {factory_type}")