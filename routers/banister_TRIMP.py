from fastapi import APIRouter, File, UploadFile, HTTPException
from sport_activities_features.training_loads import BanisterTRIMP
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from models.models import FileModel

metadata = []


router = APIRouter(prefix="/trainingLoadBannister",
    tags=["Training load calculator"])

@router.post("/", response_model=FileModel)
async def training_load(duration:float, average_heartrate:float):
    TRIMP = BanisterTRIMP(duration, average_heartrate)
    return JSONResponse(content=TRIMP.calculate_TRIMP())


