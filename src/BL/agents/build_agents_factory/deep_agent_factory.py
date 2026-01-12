


from core.interfaces.IAgentFactoryBuilder import AgentBuilder
from deep_agent_builder import DeepAgentBuilder
from core.interfaces.IAgentFactoryBuilder import AgentFactory


class DeepAgentFactory(AgentFactory):
    """
    Factory to create Deep Agent Builder
    """
    def create_agent_builder(self) -> AgentBuilder:
        """Create a DeepAgentBuilder instance.  
        Returns:
            AgentBuilder: An instance of DeepAgentBuilder.
        """
        return DeepAgentBuilder()