import json
import os
from typing import List, Optional

import overpy
from fastapi import APIRouter, File, UploadFile, HTTPException, Request, Body
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sport_activities_features import IntervalIdentificationByPower, IntervalIdentificationByHeartrate, PlotData
from sport_activities_features.overpy_node_manipulation import OverpyNodesReader
from sport_activities_features.tcx_manipulation import TCXFile
from sport_activities_features.gpx_manipulation import GPXFile
from sport_activities_features.weather_identification import WeatherIdentification
import uuid
import jsonpickle
from starlette.background import BackgroundTasks
from starlette.responses import JSONResponse
from fastapi.responses import FileResponse

from helpers.file_transformer import transform_to_previous_form
from helpers.overpy_transformer import OverpyNodeHelper
from helpers.temp_file import save_temp_plot_image
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

@router.post("/identification/heartrate/image", response_class=FileResponse)
async def interval_identification_heartrate_image(minimum_time:float=30,
                                                  request: FileModel = Body(...),
                                                  background_tasks: BackgroundTasks = BackgroundTasks()):
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

    Map = PlotData()
    plot = Map.plot_intervals_in_map(activity["timestamps"], activity["distances"], all_intervals)

    name, response = save_temp_plot_image(plot)
    background_tasks.add_task(os.remove, name)

    return response


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

@router.post("/identification/power/image", response_class=FileResponse)
async def interval_identification_power_image(mass:float, minimum_time:float=30,
                                              request: FileModel = Body(...),
                                              background_tasks: BackgroundTasks = BackgroundTasks()):
    untransformed_data = jsonable_encoder(request)
    activity = transform_to_previous_form(untransformed_data)
    Intervals = IntervalIdentificationByPower(
        activity["distances"], activity["timestamps"], activity["altitudes"], mass, minimum_time
    )
    Intervals.identify_intervals()
    all_intervals = Intervals.return_intervals()

    Map = PlotData()
    plot = Map.plot_intervals_in_map(activity["timestamps"], activity["distances"], all_intervals)
    name, response = save_temp_plot_image(plot)
    background_tasks.add_task(os.remove, name)

    return response

