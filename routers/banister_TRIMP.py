from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from sport_activities_features.training_loads import BanisterTRIMP

from models.models import BannisterTRIPMModel

metadata = []

router = APIRouter(prefix="/trainingLoadBannister",
                   tags=["Training load calculator"])


@router.post("/", response_model=BannisterTRIPMModel)
async def training_load(duration: float = Query(..., description="Duration of training in minutes"),
                        average_heartrate: float = Query(..., description="Average heartrate during the exercise")):
    """
    Calculates **Bannister training load** from average heartrate (bpm) and duration (in minutes) processed exercise.
    """
    TRIMP = BanisterTRIMP(duration, average_heartrate)
    response = {"TRIPM": TRIMP.calculate_TRIMP()}
    return JSONResponse(content=response)
