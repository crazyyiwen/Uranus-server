


from core.interfaces.IAgentFactoryBuilder import AgentBuilder, AgentFactory
from BL.agents.build_agents_factory.centralized_agent_builder import CentralizedAgent


class CentralizedAgentFactory(AgentFactory):
    """
    Factory to create Common React Agent Builder
    """
    def create_agent_builder(self) -> AgentBuilder:
        """
        Create a CommonReactAgent instance.
        Returns:
            AgentBuilder: An instance of CommonReactAgent.
        """
        return CentralizedAgent()