"""Rule evaluator for conditional edges."""

from typing import Any, Dict, List

from BL.v3.interfaces.rule_evaluator import IRuleEvaluator
from BL.v3.utils.variable_resolver import VariableResolver


class RuleEvaluator(IRuleEvaluator):
    """
    Evaluates rules for conditional routing in the workflow graph.

    Supports:
    - Multiple conditions with AND/OR logic
    - Default/else rules
    - Field comparisons (equals, contains, etc.)
    """

    def __init__(self, variable_resolver: VariableResolver = None):
        """
        Initialize rule evaluator.

        Args:
            variable_resolver: Optional variable resolver for template resolution
        """
        self.variable_resolver = variable_resolver or VariableResolver()

    def evaluate_rule(
        self, rule_config: Dict[str, Any], state: Dict[str, Any]
    ) -> bool:
        """
        Evaluate a single rule condition.

        Args:
            rule_config: Rule configuration with conditions
            state: Current workflow state

        Returns:
            True if rule matches, False otherwise
        """
        if not rule_config.get("enable", True):
            return False

        conditions = rule_config.get("conditions", [])
        logic_type = rule_config.get("logicType", "AND")

        # Empty conditions = default/else rule
        if not conditions:
            return True

        results = []
        for condition in conditions:
            field = condition.get("field", "")
            operator = condition.get("operator", "")
            expected_value = condition.get("value", "")

            # Resolve field and value templates
            field_value = self.variable_resolver.resolve(field, state)
            expected_value = self.variable_resolver.resolve(expected_value, state)

            # Evaluate condition
            result = self._evaluate_condition(field_value, operator, expected_value)
            results.append(result)

        # Apply logic
        if logic_type == "AND":
            return all(results)
        elif logic_type == "OR":
            return any(results)
        elif logic_type == "default":
            return True
        else:
            return all(results) if results else True

    def evaluate_rules(
        self, rules: List[Dict[str, Any]], state: Dict[str, Any]
    ) -> str:
        """
        Evaluate multiple rules and return matching rule ID.

        Args:
            rules: List of rule configurations
            state: Current workflow state

        Returns:
            Rule ID of the first matching rule, or "default" if none match
        """
        for rule in rules:
            rule_id = rule.get("ruleId", "")
            if self.evaluate_rule(rule, state):
                return rule_id

        return "default"

    def _evaluate_condition(self, field_value: Any, operator: str, expected_value: Any) -> bool:
        """Evaluate a single condition."""
        if operator == "equals":
            return field_value == expected_value
        elif operator == "is not empty":
            return bool(field_value) and str(field_value).strip() != ""
        elif operator == "is empty":
            return not bool(field_value) or str(field_value).strip() == ""
        elif operator == "contains":
            return str(expected_value) in str(field_value)
        elif operator == "not equals":
            return field_value != expected_value
        elif operator == "greater than":
            try:
                return float(field_value) > float(expected_value)
            except (ValueError, TypeError):
                return False
        elif operator == "less than":
            try:
                return float(field_value) < float(expected_value)
            except (ValueError, TypeError):
                return False
        else:
            return False
