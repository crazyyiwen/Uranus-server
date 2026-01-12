from functools import singledispatchmethod
from langchain.agents import create_agent

from BL.agents.agents_model.model_selection import get_dynamic_model_instance
from core.interfaces.IAgents import IAgents
from BL.agents.states.state import DeepAgentState

class Agents(IAgents):
    """
    Agents builder class to create different types of agents
    """
    def __init__(self):
        """
        Initialize the Agents class.
        """
        pass

    @singledispatchmethod
    def build_agents(self, *args, **kwargs):
        """
        Build agents based on the provided arguments.
        Raises:
            NotImplementedError: If the argument types do not match any registered method.
        """
        pass

    @build_agents.register
    def _(self, model_name: str, all_tools: list, system_prompt_instruction: str):
        try:
            model = get_dynamic_model_instance(model_name, temperature=0.0)
            if model is None:
                raise ValueError(f"Failed to initialize model: {model_name}")
            self.base_agent = create_agent(
                model, all_tools, system_prompt=system_prompt_instruction, state_schema=DeepAgentState
            )
        except Exception as e:
            self.base_agent = None
    