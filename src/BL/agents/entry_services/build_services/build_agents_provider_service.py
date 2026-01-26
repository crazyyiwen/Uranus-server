


from core.constant import AgentFactoryTypes
from core.interfaces.IAgentFactoryBuilder import AgentFactory
from BL.agents.build_agents_factory.common_react_agent_factory import CommonReactAgentFactory
# from BL.agents.build_agents_factory.deep_agent_factory import DeepAgentFactory  # Commented out - deep_agent modules removed


class AgentFactoryProvider:
    """
    Provider to get the appropriate Agent Factory based on type
    """
    @staticmethod
    def get_factory(factory_type: str) -> AgentFactory:
        """
        Get the appropriate Agent Factory based on the provided type.
        Args:
            factory_type (str): The type of agent factory to retrieve.
            Returns:
            AgentFactory: An instance of the requested Agent Factory."""
        if factory_type == AgentFactoryTypes.COMMON_REACT:
            return CommonReactAgentFactory()
        elif factory_type == AgentFactoryTypes.DEEP_AGENT:
            # return DeepAgentFactory()  # Commented out - deep_agent modules removed
            pass
        else:
            raise ValueError(f"Unsupported factory type: {factory_type}")