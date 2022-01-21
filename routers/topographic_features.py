import os
import uuid
from typing import Optional

from fastapi import APIRouter, File, UploadFile, HTTPException, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sport_activities_features import ElevationIdentification, HillIdentification, TopographicFeatures
from sport_activities_features.gpx_manipulation import GPXFile
from sport_activities_features.tcx_manipulation import TCXFile

from helpers.file_transformer import transform_to_previous_form
from models.models import FileModel, AltitudeModel, HillDataModel

metadata = []

router = APIRouter(prefix="/topographicFeatures",
                   tags=["Topographic features"])


@router.post("/", response_model=HillDataModel)
async def topographic_features(ascent_threshold: Optional[int] = None, request: FileModel = Body(...)):
    untransformed_data = jsonable_encoder(request)
    standardized_data = transform_to_previous_form(untransformed_data)
    if(ascent_threshold==None):
        ascent_threshold=30

    Hill = HillIdentification(standardized_data["altitudes"], ascent_threshold)
    Hill.identify_hills()
    all_hills = Hill.return_hills()

    # extract features from data
    Top = TopographicFeatures(all_hills)
    num_hills = Top.num_of_hills()
    avg_altitude = Top.avg_altitude_of_hills(standardized_data["altitudes"])
    avg_ascent = Top.avg_ascent_of_hills(standardized_data["altitudes"])
    distance_hills = Top.distance_of_hills(standardized_data["positions"])
    hills_share = Top.share_of_hills(distance_hills, standardized_data["total_distance"])

    data = {
        "number_of_hills": num_hills,
        "average_altitude": avg_altitude,
        "average_ascent": avg_ascent,
        "total_distance": distance_hills,
        "total_distance_hills": distance_hills,
        "hills_share": hills_share,
    }

    return JSONResponse(content=jsonable_encoder(data))
