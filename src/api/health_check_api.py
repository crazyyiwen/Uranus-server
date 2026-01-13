from fastapi import APIRouter
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