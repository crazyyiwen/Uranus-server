"""Demo API: triggers V3 workflow agent with user input (async)."""

from core.constant import AGENTIC_WORKFLOW_JSON_PATH_SIMPLE
from core.helper.exception_dispatch_service import catch_exception
from core.models.return_model import ReturnModel
from fastapi import APIRouter, Request

from BL.v3.workflow_builder import (
    ainvoke_workflow,
    build_initial_state_from_user_input,
    get_v3_graph_for_file,
)

router = APIRouter()


@router.post("/v3/invoke")
async def v3_agent_invoke(request: Request):
    """
    Trigger the V3 workflow agent with user input.

    Request body:
    {
        "query": "User message or question"  // required
    }

    Returns:
        Final workflow state (messages, flow, nodes, etc.)
    """
    try:
        body = await request.json()
        query = body.get("query") or body.get("message") or ""
        if not query.strip():
            return ReturnModel(
                {"error": "Missing or empty 'query' or 'message' in request body"},
                400,
            )

        graph = get_v3_graph_for_file(str(AGENTIC_WORKFLOW_JSON_PATH_SIMPLE))
        initial_state = build_initial_state_from_user_input(query)

        result = await ainvoke_workflow(graph, initial_state)
        return ReturnModel(result, 200)
    except Exception as ex:
        return catch_exception(ex)


@router.post("/example_basic_workflow")
async def demo_agent(request: Request):
    """
    Same as /v3/invoke: runs V3 workflow with user input from body.

    Request body:
    {
        "query": "User message or question"
    }
    """
    try:
        body = await request.json()
        query = body.get("query") or body.get("message") or "I want to amend a contract"

        graph = get_v3_graph_for_file(str(AGENTIC_WORKFLOW_JSON_PATH_SIMPLE))
        initial_state = build_initial_state_from_user_input(query)

        result = await ainvoke_workflow(graph, initial_state)
        return ReturnModel(result, 200)
    except Exception as ex:
        return catch_exception(ex)
