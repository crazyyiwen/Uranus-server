from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/api/healthcheck")
def root():
    time_zone = str(datetime.now())
    return {
        "message": f'Current time zone {time_zone}',
        "time_started": f'Up and running Uranus server',
        "version": '0.1'
    }