"""Variable resolver implementation for template resolution and state updates."""

import re
from typing import Any, Dict, List

from BL.v3.interfaces.variable_resolver import IVariableResolver


class VariableResolver(IVariableResolver):
    """
    Resolves template variables and applies variable updates to state.

    Supports:
    - {{flow.variableName}} - flow-scoped variables
    - {{system.variableName}} - system-scoped variables
    - {{nodes.nodeId.outputField}} - node outputs
    - {{nodeOutput.field}} - current node output
    """

    TEMPLATE_PATTERN = re.compile(r"\{\{([^}]+)\}\}")

    def resolve(self, template: str, state: Dict[str, Any]) -> Any:
        """
        Resolve template string with state variables.

        Args:
            template: Template string like "{{flow.agentId}}"
            state: Current workflow state

        Returns:
            Resolved value
        """
        if not isinstance(template, str):
            return template

        def replace_match(match):
            expr = match.group(1).strip()
            return str(self._evaluate_expression(expr, state))

        resolved = self.TEMPLATE_PATTERN.sub(replace_match, template)

        # Try to parse as number/boolean if no templates were found
        if resolved == template and resolved not in ["", None]:
            try:
                # Try boolean
                if resolved.lower() in ["true", "false"]:
                    return resolved.lower() == "true"
                # Try number
                if "." in resolved:
                    return float(resolved)
                return int(resolved)
            except ValueError:
                pass

        return resolved

    def _evaluate_expression(self, expr: str, state: Dict[str, Any]) -> Any:
        """
        Evaluate a single expression like "flow.agentId" or "nodes.nodeId.output".

        Args:
            expr: Expression to evaluate
            state: Current state

        Returns:
            Resolved value or empty string if not found
        """
        parts = expr.split(".")

        if len(parts) == 0:
            return ""

        # Handle flow variables
        if parts[0] == "flow":
            flow = state.get("flow", {})
            if len(parts) == 2:
                return flow.get(parts[1], "")
            return self._nested_get(flow, parts[1:], "")

        # Handle system variables
        if parts[0] == "system":
            system = state.get("system", {})
            if len(parts) == 2:
                return system.get(parts[1], "")
            return self._nested_get(system, parts[1:], "")

        # Handle node outputs: nodes.nodeId.field
        if parts[0] == "nodes" and len(parts) >= 2:
            nodes = state.get("nodes", {})
            node_id = parts[1]
            if node_id in nodes:
                node_output = nodes[node_id]
                if len(parts) == 2:
                    return node_output
                return self._nested_get(node_output, parts[2:], "")

        # Handle nodeOutput (current node output)
        if parts[0] == "nodeOutput":
            node_output = state.get("nodeOutput", {})
            if len(parts) == 1:
                return node_output
            return self._nested_get(node_output, parts[1:], "")

        # Handle interface inputs
        if parts[0] == "interface" and len(parts) >= 2:
            interface = state.get("interface", {})
            if parts[1] == "inputs":
                inputs = interface.get("inputs", {})
                if len(parts) == 3:
                    return inputs.get(parts[2], "")
                return self._nested_get(inputs, parts[2:], "")

        return ""

    def _nested_get(self, obj: Dict[str, Any], path: List[str], default: Any = None) -> Any:
        """Get nested value from dictionary using path list."""
        current = obj
        for part in path:
            if isinstance(current, dict):
                current = current.get(part)
                if current is None:
                    return default
            else:
                return default
        return current if current is not None else default

    def apply_variable_updates(
        self, updates: List[Dict[str, Any]], node_output: Dict[str, Any], state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Apply variable updates to state based on node output.

        Args:
            updates: List of variable update definitions
            node_output: Output from the node
            state: Current state

        Returns:
            Updated state
        """
        updated_state = {**state}
        updated_state["nodeOutput"] = node_output

        # Ensure nested structures exist
        if "flow" not in updated_state:
            updated_state["flow"] = {}
        if "system" not in updated_state:
            updated_state["system"] = {}
        if "nodes" not in updated_state:
            updated_state["nodes"] = {}

        for update in updates:
            # Check if update has rules (conditional update)
            if "rules" in update:
                if not self._evaluate_update_rules(update["rules"], updated_state):
                    continue

            field_name = update.get("fieldName", "")
            operation = update.get("operation", "set")
            value_template = update.get("value", "")

            # Resolve value template
            value = self.resolve(value_template, updated_state)

            # Apply operation
            self._apply_update(updated_state, field_name, operation, value, update)

        return updated_state

    def _evaluate_update_rules(self, rules: Dict[str, Any], state: Dict[str, Any]) -> bool:
        """Evaluate rules for conditional variable updates."""
        conditions = rules.get("conditions", [])
        logic_type = rules.get("logicType", "AND")

        if not conditions:
            return True

        results = []
        for condition in conditions:
            field = condition.get("field", "")
            operator = condition.get("operator", "")
            expected_value = condition.get("value", "")

            # Resolve field and value
            field_value = self.resolve(field, state)
            expected_value = self.resolve(expected_value, state)

            # Evaluate condition
            result = self._evaluate_condition(field_value, operator, expected_value)
            results.append(result)

        # Apply logic
        if logic_type == "AND":
            return all(results)
        elif logic_type == "OR":
            return any(results)
        else:
            return all(results) if results else True

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
        else:
            return False

    def _apply_update(
        self,
        state: Dict[str, Any],
        field_name: str,
        operation: str,
        value: Any,
        update_config: Dict[str, Any],
    ) -> None:
        """Apply a single variable update operation."""
        parts = field_name.split(".")
        if len(parts) < 2:
            return

        scope = parts[0]  # flow, system, thread, etc.
        field_path = parts[1:]

        if scope == "flow":
            target = state["flow"]
        elif scope == "system":
            target = state["system"]
        elif scope == "thread":
            # Handle thread.messages specially
            if len(field_path) == 1 and field_path[0] == "messages":
                if "messages" not in state:
                    state["messages"] = []
                messages = state["messages"]
                role = update_config.get("role", "user")
                if operation == "append":
                    messages.append({"content": value, "role": role})
                elif operation == "extend":
                    if isinstance(value, list):
                        messages.extend([{"content": v, "role": role} for v in value])
                    else:
                        messages.append({"content": value, "role": role})
                return
            else:
                if "thread" not in state:
                    state["thread"] = {}
                target = state["thread"]
        else:
            return

        # Navigate to target field
        current = target
        for i, part in enumerate(field_path[:-1]):
            if part not in current:
                current[part] = {}
            current = current[part]

        final_field = field_path[-1]

        # Apply operation
        if operation == "set":
            current[final_field] = value
        elif operation == "append":
            if final_field not in current:
                current[final_field] = []
            if isinstance(current[final_field], list):
                current[final_field].append(value)
        elif operation == "extend":
            if final_field not in current:
                current[final_field] = []
            if isinstance(current[final_field], list):
                if isinstance(value, list):
                    current[final_field].extend(value)
                else:
                    current[final_field].append(value)
