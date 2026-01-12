from core.helper.exception_dispatch_service import catch_exception
from fastapi import APIRouter, Request
from core.models.return_model import ReturnModel
from BL.buyer_agent_service import buyeragentmock

router = APIRouter()

    
@router.post("/buyer_agent_mock")
async def buyer_agent_mock(request: Request):
    try:
        result = await buyeragentmock(request).mock_process()
        return ReturnModel(result, 200)
    except Exception as ex:
        return catch_exception(ex)