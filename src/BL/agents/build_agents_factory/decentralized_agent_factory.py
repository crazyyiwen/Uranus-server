


from core.interfaces.IAgentFactoryBuilder import AgentBuilder
from decentralized_agent_builder import DecentralizedAgentBuilder
from core.interfaces.IAgentFactoryBuilder import AgentFactory


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