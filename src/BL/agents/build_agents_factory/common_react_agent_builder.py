


from BL.agents.entry_services.build_services.build_agent_workflow_service import build_langgraph_agents_from_file
from core.interfaces.IAgentFactoryBuilder import AgentBuilder


class CommonReactAgent(AgentBuilder):
    """
    Builder for Common React Agents
    """
    def build_dynamic_agents(self, path: str):
        """
        Build dynamic agents from a given JSON workflow file.
        Args:
            path (str): Path to the JSON workflow file.
            Returns:
            Any: The constructed agent graph or structure.
        """
        return build_langgraph_agents_from_file(path=path)

    def build_agents_with_mcp(self) -> None:
        """
        Build agents using MCP (Multi-Channel Processing) approach.
        Returns:
            None
        """
        pass