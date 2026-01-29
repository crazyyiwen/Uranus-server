"""Executor for rule nodes."""

from typing import Any, Dict

from BL.v3.nodes.executors.base_executor import BaseNodeExecutor
from BL.v3.utils.rule_evaluator import RuleEvaluator


class RuleNodeExecutor(BaseNodeExecutor):
    """Executor for rule nodes - evaluates conditions for routing."""

    def __init__(self, variable_resolver=None):
        """Initialize rule executor."""
        super().__init__(variable_resolver)
        self.rule_evaluator = RuleEvaluator(variable_resolver)

    async def execute(self, node_config: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute rule node - evaluates rules and returns matching rule ID (async).

        Args:
            node_config: Rule node configuration
            state: Current state

        Returns:
            Dictionary with matched rule ID
        """
        rules = node_config.get("config", {}).get("rules", [])
        matched_rule_id = self.rule_evaluator.evaluate_rules(rules, state)

        output = {
            "matchedRuleId": matched_rule_id,
            "rules": rules,
        }

        # Apply variable updates if any
        updated_state = self._apply_variable_updates(output, node_config, state)

        return {
            "output": output,
            "state": updated_state,
            "matchedRuleId": matched_rule_id,  # For routing
        }

    def get_output_schema(self) -> Dict[str, Any]:
        """Return output schema for rule node."""
        return {
            "type": "object",
            "properties": {
                "matchedRuleId": {"type": "string"},
            },
        }
