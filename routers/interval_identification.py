import json
from typing import List, Optional

import overpy
from fastapi import APIRouter, File, UploadFile, HTTPException, Request, Body
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sport_activities_features import IntervalIdentificationByPower, IntervalIdentificationByHeartrate
from sport_activities_features.overpy_node_manipulation import OverpyNodesReader
from sport_activities_features.tcx_manipulation import TCXFile
from sport_activities_features.gpx_manipulation import GPXFile
from sport_activities_features.weather_identification import WeatherIdentification
import uuid
import jsonpickle
from starlette.responses import JSONResponse

from helpers.file_transformer import transform_to_previous_form
from helpers.overpy_transformer import OverpyNodeHelper
from models.models import FileModel, NodeModel, IntervalModel

metadata = []


router = APIRouter(prefix="/interval",
    tags=["interval"])


@router.post("/identification/heartrate", response_model=IntervalModel)
async def interval_identification_heartrate(minimum_time:float=30, request: FileModel = Body(...)):
    untransformed_data = jsonable_encoder(request)
    activity = transform_to_previous_form(untransformed_data)
    Intervals = IntervalIdentificationByHeartrate(
        activity["distances"],
        activity["timestamps"],
        activity["altitudes"],
        activity["heartrates"],
        minimum_time
    )

    Intervals.identify_intervals()
    all_intervals = Intervals.return_intervals()

    data = {
        'intervals': all_intervals,
        'statistics':Intervals.calculate_interval_statistics()
    }
    return JSONResponse(content=jsonable_encoder(data))


@router.post("/identification/power", response_model=IntervalModel)
async def interval_identification_power(mass:float, minimum_time:float=30, request: FileModel = Body(...)):
    untransformed_data = jsonable_encoder(request)
    activity = transform_to_previous_form(untransformed_data)
    Intervals = IntervalIdentificationByPower(
        activity["distances"], activity["timestamps"], activity["altitudes"], mass, minimum_time
    )
    Intervals.identify_intervals()
    all_intervals = Intervals.return_intervals()

    data = {
        'intervals': all_intervals,
        'statistics': Intervals.calculate_interval_statistics()
    }
    return JSONResponse(content=jsonable_encoder(data))


