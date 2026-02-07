"""
Demo tool implementations for agentic_workflow_simple.json.

Handoff and tool node demo functions; each logs when called and returns
a simple response so the workflow can verify the related tool was invoked.
"""

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)
DEMO_LOGS: List[Dict[str, Any]] = []


def _log(tool_name: str, message: str, params: Dict[str, Any] = None) -> None:
    DEMO_LOGS.append({"tool": tool_name, "message": message, "params": params or {}})
    logger.info("[DEMO TOOL CALLED] %s - %s", tool_name, message)


# Handoff tools (supervisor agent)
def demo_supplier_validation_handoff(**kwargs: Any) -> Dict[str, Any]:
    _log("supplier_validation_handoff", "Handoff tool supplier_validation_handoff was called.", kwargs)
    return {"called": True, "tool": "supplier_validation_handoff", "message": "Completed step 1 and waiting for user interaction"}


def demo_confirmation(**kwargs: Any) -> Dict[str, Any]:
    _log("confirmation", "Handoff tool confirmation was called.", kwargs)
    return {"called": True, "tool": "confirmation", "message": "Completed step 2 and waiting for user interaction"}


def demo_offboarding_reason_handoff(**kwargs: Any) -> Dict[str, Any]:
    _log("offboarding_reason_handoff", "Handoff tool offboarding_reason_handoff was called.", kwargs)
    return {"called": True, "tool": "offboarding_reason_handoff", "message": "Completed step 3 and waiting for user interaction"}


def demo_summary_confirmation_handoff(**kwargs: Any) -> Dict[str, Any]:
    _log("summary_confirmation_handoff", "Handoff tool summary_confirmation_handoff was called.", kwargs)
    return {"called": True, "tool": "summary_confirmation_handoff", "message": "Completed step 4 and waiting for user interaction"}


def demo_request_creation_handoff(**kwargs: Any) -> Dict[str, Any]:
    _log("request_creation_handoff", "Handoff tool request_creation_handoff was called.", kwargs)
    return {"called": True, "tool": "request_creation_handoff", "message": "Completed step 5 and waiting for user interaction"}


def demo_complete_step(**kwargs: Any) -> Dict[str, Any]:
    _log("complete_step", "Handoff tool complete_step was called.", kwargs)
    return {"called": True, "tool": "complete_step", "message": "complete_step executed"}


# Tool nodes
def demo_getsuppliers(**kwargs: Any) -> Dict[str, Any]:
    _log("getsuppliers", "Tool node getsuppliers was called.", kwargs)
    return {"called": True, "tool": "getsuppliers", "log": "Tool node getsuppliers was called."}


def demo_suppliergridv1(**kwargs: Any) -> Dict[str, Any]:
    _log("suppliergridv1", "Tool node suppliergridv1 was called.", kwargs)
    return {"called": True, "tool": "suppliergridv1", "log": "Tool node suppliergridv1 was called."}


def demo_labelandbuttons(**kwargs: Any) -> Dict[str, Any]:
    _log("labelandbuttons", "Tool node labelandbuttons was called.", kwargs)
    return {"called": True, "tool": "labelandbuttons", "log": "Tool node labelandbuttons was called."}


def demo_labelandbuttons1(**kwargs: Any) -> Dict[str, Any]:
    _log("labelandbuttons1", "Tool node labelandbuttons1 was called.", kwargs)
    return {"called": True, "tool": "labelandbuttons1", "log": "Tool node labelandbuttons1 was called."}


def demo_labelandbuttons2(**kwargs: Any) -> Dict[str, Any]:
    _log("labelandbuttons2", "Tool node labelandbuttons2 was called.", kwargs)
    return {"called": True, "tool": "labelandbuttons2", "log": "Tool node labelandbuttons2 was called."}


def demo_labelandbuttons4(**kwargs: Any) -> Dict[str, Any]:
    _log("labelandbuttons4", "Tool node labelandbuttons4 was called.", kwargs)
    return {"called": True, "tool": "labelandbuttons4", "log": "Tool node labelandbuttons4 was called."}


def demo_getglobalcode(**kwargs: Any) -> Dict[str, Any]:
    _log("getglobalcode", "Tool node getglobalcode was called.", kwargs)
    return {"called": True, "tool": "getglobalcode", "log": "Tool node getglobalcode was called."}


def demo_projectrequesttool(**kwargs: Any) -> Dict[str, Any]:
    _log("projectrequesttool", "Tool node projectrequesttool was called.", kwargs)
    return {"called": True, "tool": "projectrequesttool", "log": "Tool node projectrequesttool was called."}


def demo_prfcreaterequestformpv(**kwargs: Any) -> Dict[str, Any]:
    _log("prfcreaterequestformpv", "Tool node prfcreaterequestformpv was called.", kwargs)
    return {"called": True, "tool": "prfcreaterequestformpv", "log": "Tool node prfcreaterequestformpv was called."}


DEMO_TOOLS_REGISTRY: Dict[str, Any] = {
    "supplier_validation_handoff": demo_supplier_validation_handoff,
    "confirmation": demo_confirmation,
    "offboarding_reason_handoff": demo_offboarding_reason_handoff,
    "summary_confirmation_handoff": demo_summary_confirmation_handoff,
    "request_creation_handoff": demo_request_creation_handoff,
    "complete_step": demo_complete_step,
    "getsuppliers": demo_getsuppliers,
    "suppliergridv1": demo_suppliergridv1,
    "labelandbuttons": demo_labelandbuttons,
    "labelandbuttons1": demo_labelandbuttons1,
    "labelandbuttons2": demo_labelandbuttons2,
    "labelandbuttons4": demo_labelandbuttons4,
    "getglobalcode": demo_getglobalcode,
    "projectrequesttool": demo_projectrequesttool,
    "prfcreaterequestformpv": demo_prfcreaterequestformpv,
}


def get_demo_tool(name: str):
    return DEMO_TOOLS_REGISTRY.get(name)


def get_demo_logs(clear: bool = False) -> List[Dict[str, Any]]:
    logs = list(DEMO_LOGS)
    if clear:
        DEMO_LOGS.clear()
    return logs


def call_demo_tool(tool_name: str, **kwargs: Any) -> Dict[str, Any]:
    fn = DEMO_TOOLS_REGISTRY.get(tool_name)
    if fn is None:
        _log(tool_name, "Demo tool not found in registry.", kwargs)
        return {"called": False, "tool": tool_name, "error": "Unknown tool: " + tool_name}
    return fn(**kwargs)


def was_tool_called(tool_name: str) -> bool:
    return any(entry.get("tool") == tool_name for entry in DEMO_LOGS)
