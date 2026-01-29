"""Executor for LLM nodes (standalone LLM calls)."""

from typing import Any, Dict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from BL.agents.agents_model.model_selection import get_dynamic_model_instance, get_default_model_name
from BL.v3.nodes.executors.base_executor import BaseNodeExecutor


class LLMNodeExecutor(BaseNodeExecutor):
    """Executor for standalone LLM nodes."""

    async def execute(self, node_config: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute LLM node (async).

        Args:
            node_config: LLM node configuration
            state: Current state

        Returns:
            LLM output
        """
        config = node_config.get("config", {})

        # Get model configuration
        model_config = config.get("model", {})
        model_code = model_config.get("code", "gpt-4.1")
        model_name = get_default_model_name(model_code)

        # Initialize LLM
        llm = get_dynamic_model_instance(model_name, temperature=0.0)

        # Get prompt
        prompt_template = config.get("prompt", "")
        prompt = self.variable_resolver.resolve(prompt_template, state)

        # Invoke LLM (async)
        response = await llm.ainvoke([HumanMessage(content=prompt)])

        # Extract response
        response_content = response.content if hasattr(response, "content") else str(response)

        output = {
            "text": response_content,
            "prompt": prompt,
        }

        # Apply variable updates
        updated_state = self._apply_variable_updates(output, node_config, state)

        return {
            "output": output,
            "state": updated_state,
        }

    def get_output_schema(self) -> Dict[str, Any]:
        """Return output schema for LLM node."""
        return {
            "type": "object",
            "properties": {
                "text": {"type": "string"},
            },
        }
