


from BL.agents.build_tools.tools_factory_service import CentralizedAgentToolsFactory, DecentralizedAgentToolsFactory
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
        if factory_type == ToolsFactoryTypes.CENTRALIZED_AGENT:
            return CentralizedAgentToolsFactory()
        elif factory_type == ToolsFactoryTypes.DECENTRALIZED_AGENT:
            return DecentralizedAgentToolsFactory()
            pass
        else:
            raise ValueError(f"Unsupported factory type: {factory_type}")