import os
import uuid
from typing import Optional

from fastapi import APIRouter, File, UploadFile, HTTPException, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sport_activities_features import ElevationIdentification
from sport_activities_features.gpx_manipulation import GPXFile
from sport_activities_features.interruptions.interruption_processor import InterruptionProcessor
from sport_activities_features.tcx_manipulation import TCXFile

from helpers.file_transformer import transform_to_previous_form
from models.models import FileModel, AltitudeModel

metadata = []

router = APIRouter(prefix="/interruption",
                   tags=["Interruption identification"])


@router.post("/identification/", response_model=FileModel)
async def identify_interruptions(overpass_api_url: Optional[str] = "https://lz4.overpass-api.de/api/interpreter", time_interval:Optional[float]=60, min_speed:Optional[float]=2, intersectionsIdentificator:Optional[bool] = True, request: FileModel = Body(...)):
    untransformed_data = jsonable_encoder(request)
    standardized_data = transform_to_previous_form(untransformed_data)

    interruptionProcessor = InterruptionProcessor(time_interval, min_speed,overpass_api_url)

    events = interruptionProcessor.events(standardized_data, True)

    standardized_data.update({'events':events})

    return JSONResponse(content=jsonable_encoder(standardized_data))


