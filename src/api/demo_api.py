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
from core.utils.common_functions import get_file_path

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
        
        # should change file name dynamically
        file_path = get_file_path("all.json")
        # end
        graph = await get_v3_graph_for_file(file_path)
        initial_state = build_initial_state_from_user_input(query)

        result = await ainvoke_workflow(graph, initial_state)
        return ReturnModel(result, 200)
    except Exception as ex:
        return catch_exception(ex)
