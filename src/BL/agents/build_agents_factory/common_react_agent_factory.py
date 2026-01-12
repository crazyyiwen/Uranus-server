


from core.interfaces.IAgentFactoryBuilder import AgentBuilder, AgentFactory
from BL.agents.build_agents_factory.common_react_agent_builder import CommonReactAgent


class CommonReactAgentFactory(AgentFactory):
    """
    Factory to create Common React Agent Builder
    """
    def create_agent_builder(self) -> AgentBuilder:
        """
        Create a CommonReactAgent instance.
        Returns:
            AgentBuilder: An instance of CommonReactAgent.
        """
        return CommonReactAgent()