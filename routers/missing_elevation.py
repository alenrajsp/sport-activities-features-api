from typing import Optional

from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sport_activities_features import ElevationIdentification

from helpers.file_transformer import transform_to_previous_form
from models.models import FileModel

metadata = []

router = APIRouter(prefix="/elevation",
                   tags=["Elevation identification"])


@router.post("/identification/", response_model=FileModel)
async def missing_elevation_identification(open_elevation_api: Optional[str] = None, request: FileModel = Body(...)):
    """
    Identifies elevation (in meters) for each point of a recorded exercise (sent in JSON processed format)
    and adds it to the JSON object.
    """
    untransformed_data = jsonable_encoder(request)
    standardized_data = transform_to_previous_form(untransformed_data)

    if (open_elevation_api == None):
        open_elevation_api = "https://api.open-elevation.com/api/v1/lookup"

    elevations = ElevationIdentification(standardized_data['positions'], open_elevation_api)
    standardized_data.update({'altitudes': elevations})

    return JSONResponse(content=jsonable_encoder(standardized_data))
