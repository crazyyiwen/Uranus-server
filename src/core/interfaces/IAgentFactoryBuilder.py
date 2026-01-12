

from abc import ABC, abstractmethod


class AgentBuilder(ABC):

    @abstractmethod
    def build_dynamic_agents(self, path: str):
        """Build agents from agentic workflow JSON file

        Args:
            path: Path to the agentic_workflow.json file

        Returns:
            Compiled agent graph
        """
        pass

    @abstractmethod
    def build_agents_with_mcp(self) -> None:
        """Build agents from agentic workflow JSON file

        Args:
            path: Path to the agentic_workflow.json file

        Returns:
            Compiled agent graph with mcp
        """
        pass



class AgentFactory(ABC):

    @abstractmethod
    def create_agent_builder(self) -> AgentBuilder:
        """Create an agent builder instance

        Args:
            self: class itself

        Returns:
            agent builder instance
        """
        pass