"""Interface for rule evaluation."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class IRuleEvaluator(ABC):
    """Interface for evaluating conditional rules."""

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass
