



from core.interfaces.IAgentFactoryBuilder import AgentBuilder


class DecentralizedAgentBuilder(AgentBuilder):
    """
    Builder for Deep Agents
    """
    def build_dynamic_agents(self, path: str):
        """
        Build dynamic agents from a given JSON workflow file.
        Args:
            path (str): Path to the JSON workflow file.
        Returns:
            Any: The constructed agent graph or structure.
        """
        pass

    def build_agents_with_mcp(self) -> None:
        """
        Build agents using MCP (Multi-Channel Processing) approach.
        Returns:
            None
        """
        pass