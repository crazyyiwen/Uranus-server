"""Executor for agent nodes."""

from typing import Any, Dict, List

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from BL.agents.agents_model.model_selection import get_dynamic_model_instance, get_default_model_name
from BL.v3.nodes.executors.base_executor import BaseNodeExecutor


class AgentNodeExecutor(BaseNodeExecutor):
    """Executor for agent nodes - LLM-based reasoning agents."""

    async def execute(self, node_config: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute agent node - runs LLM with tools and prompts (async).

        Args:
            node_config: Agent node configuration
            state: Current state

        Returns:
            Agent output dictionary
        """
        config = node_config.get("config", {})

        # Get model configuration
        model_config = config.get("model", {})
        model_code = model_config.get("code", "gpt-4.1")
        model_name = get_default_model_name(model_code)

        # Initialize LLM
        llm = get_dynamic_model_instance(model_name, temperature=0.0)

        # Build system message from prompt templates
        prompt_templates = config.get("promptTemplate", [])
        
        system_message = self._build_system_message(prompt_templates)

        # Get messages from state
        messages = state.get("messages", [])
        if not messages:
            user_query = state.get("system", {}).get("userQuery", "")
            if user_query:
                messages = [HumanMessage(content=user_query)]

        # Build message list with system message
        langchain_messages = []
        if system_message:
            langchain_messages.append(SystemMessage(content=system_message))

        # Convert state messages to LangChain messages
        for msg in messages:
            if isinstance(msg, dict):
                role = msg.get("role", "user")
                content = msg.get("content", "")
                if role == "user":
                    langchain_messages.append(HumanMessage(content=content))
                elif role == "assistant":
                    langchain_messages.append(AIMessage(content=content))
            else:
                langchain_messages.append(msg)

        # Get tools (if any) - simplified for now
        tools = config.get("tools", [])
        llm_with_tools = llm
        if tools:
            # In a full implementation, tools would be built and bound here
            # For now, we'll use the LLM without tools
            pass

        # Invoke LLM (async)
        response = await llm_with_tools.ainvoke(langchain_messages)

        # Extract response content
        response_content = response.content if hasattr(response, "content") else str(response)

        # Build output
        output = {
            "text": response_content,
            "messages": [{"role": "assistant", "content": response_content}],
        }

        # Apply variable updates
        updated_state = self._apply_variable_updates(output, node_config, state)

        # Add to messages in state
        if "messages" not in updated_state:
            updated_state["messages"] = []
        updated_state["messages"].append({"role": "assistant", "content": response_content})

        return {
            "output": output,
            "state": updated_state,
        }

    def _build_system_message(self, prompt_templates: List[Dict[str, Any]]) -> str:
        """Build system message from prompt templates."""
        system_parts = []
        for template in prompt_templates:
            if template.get("role") == "system":
                system_parts.append(template.get("text", ""))
        return "\n".join(system_parts)

    def get_output_schema(self) -> Dict[str, Any]:
        """Return output schema for agent node."""
        return {
            "type": "object",
            "properties": {
                "text": {"type": "string"},
                "messages": {"type": "array"},
            },
        }
