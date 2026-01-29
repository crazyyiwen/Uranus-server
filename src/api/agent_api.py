from BL.agents.entry_services.agent_service import agent_invoke_simple, agent_invoke_complex
from core.helper.exception_dispatch_service import catch_exception
from fastapi import APIRouter, Request
from core.models.return_model import ReturnModel

router = APIRouter()

    
@router.post("/agent_invoke_simple")
async def buyer_agent_mock(request: Request):
    try:
        result = await agent_invoke_simple(request)
        return ReturnModel(result, 200)
    except Exception as ex:
        return catch_exception(ex)

@router.post("/agent_invoke_complex")
async def buyer_agent_mock(request: Request):
    try:
        result = await agent_invoke_complex(request)
        return ReturnModel(result, 200)
    except Exception as ex:
        return catch_exception(ex)