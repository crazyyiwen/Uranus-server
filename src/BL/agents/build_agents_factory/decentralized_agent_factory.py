


from core.interfaces.IAgentFactoryBuilder import AgentBuilder, AgentFactory
from BL.agents.build_agents_factory.decentralized_agent_builder import DecentralizedAgentBuilder


class DecentralizedAgentFactory(AgentFactory):
    """
    Factory to create Deep Agent Builder
    """
    def create_agent_builder(self) -> AgentBuilder:
        """Create a DeepAgentBuilder instance.  
        Returns:
            AgentBuilder: An instance of DeepAgentBuilder.
        """
        return DecentralizedAgentBuilder()