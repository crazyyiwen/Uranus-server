"""Register all node executors with the registry."""

from BL.v3.nodes.executors.agent_executor import AgentNodeExecutor
from BL.v3.nodes.executors.http_executor import HttpRequestNodeExecutor
from BL.v3.nodes.executors.llm_executor import LLMNodeExecutor
from BL.v3.nodes.executors.output_executor import OutputNodeExecutor
from BL.v3.nodes.executors.rule_executor import RuleNodeExecutor
from BL.v3.nodes.executors.start_executor import StartNodeExecutor
from BL.v3.nodes.executors.tool_executor import ToolNodeExecutor
from BL.v3.nodes.executors.variable_update_executor import VariableUpdateNodeExecutor
from BL.v3.nodes.executors.workflow_executor import WorkflowNodeExecutor
from BL.v3.nodes.node_registry import NodeRegistry


def register_all_nodes():
    """Register all node executors with the registry."""
    NodeRegistry.register("start", StartNodeExecutor)
    NodeRegistry.register("output", OutputNodeExecutor)
    NodeRegistry.register("agent", AgentNodeExecutor)
    NodeRegistry.register("workflow", WorkflowNodeExecutor)
    NodeRegistry.register("rule", RuleNodeExecutor)
    NodeRegistry.register("llm", LLMNodeExecutor)
    NodeRegistry.register("http request", HttpRequestNodeExecutor)
    NodeRegistry.register("http-request", HttpRequestNodeExecutor)  # Alternative naming
    NodeRegistry.register("variable update", VariableUpdateNodeExecutor)
    NodeRegistry.register("variable-update", VariableUpdateNodeExecutor)  # Alternative naming
    NodeRegistry.register("tool", ToolNodeExecutor)
    # Note: Guardrail can be added later as needed


# Auto-register on import
register_all_nodes()
