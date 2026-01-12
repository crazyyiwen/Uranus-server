from BL.document_duplication_check_service import WorkFlowExe
from core.helper.exception_dispatch_service import catch_exception
from fastapi import APIRouter, Request
from core.models.return_model import ReturnModel
from datetime import datetime

router = APIRouter()

@router.get("/api/healthcheck")
def root():
    time_zone = str(datetime.now())
    return {
        "message": f'Current time zone {time_zone}',
        "time_started": f'Up and running Leo P2P Common AI apis',
        "version": '0.1'
    }