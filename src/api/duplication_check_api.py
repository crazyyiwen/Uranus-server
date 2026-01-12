from BL.document_duplication_check_service import WorkFlowExe
from core.helper.exception_dispatch_service import catch_exception
from fastapi import APIRouter, Request
from core.models.return_model import ReturnModel

router = APIRouter()

    
@router.post("/document_duplication_check")
async def document_duplication_check(request: Request):
    try:
        result = await WorkFlowExe(request).check_exe()
        return ReturnModel(result, 200)
    except Exception as ex:
        return catch_exception(ex)