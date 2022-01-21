import os
import uuid
from typing import Optional

from fastapi import APIRouter, File, UploadFile, HTTPException, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sport_activities_features import ElevationIdentification
from sport_activities_features.gpx_manipulation import GPXFile
from sport_activities_features.tcx_manipulation import TCXFile

from helpers.file_transformer import transform_to_previous_form
from models.models import FileModel, AltitudeModel

metadata = []

router = APIRouter(prefix="/elevation",
                   tags=["Elevation identification"])


@router.post("/identification/", response_model=FileModel)
async def missing_elevation_identification(open_elevation_api: Optional[str] = None, request: FileModel = Body(...)):
    untransformed_data = jsonable_encoder(request)
    standardized_data = transform_to_previous_form(untransformed_data)

    if(open_elevation_api == None):
        open_elevation_api="https://api.open-elevation.com/api/v1/lookup"


    elevations = ElevationIdentification(standardized_data['positions'], open_elevation_api)
    standardized_data.update({'altitudes':elevations})

    return JSONResponse(content=jsonable_encoder(standardized_data))


