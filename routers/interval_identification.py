import json
import os
from typing import List, Optional

import overpy
from fastapi import APIRouter, File, UploadFile, HTTPException, Request, Body
from fastapi.encoders import jsonable_encoder
from sport_activities_features import PlotData
from sport_activities_features.interval_identification import IntervalIdentificationByHeartRate, IntervalIdentificationByPower
from starlette.background import BackgroundTasks
from starlette.responses import JSONResponse
from fastapi.responses import FileResponse

from helpers.file_transformer import transform_to_previous_form
from helpers.temp_file import save_temp_plot_image
from models.models import FileModel, IntervalModel

metadata = []


router = APIRouter(prefix="/interval",
    tags=["interval"])


@router.post("/identification/heartrate", response_model=IntervalModel)
async def interval_identification_heartrate(minimum_time:float=30, request: FileModel = Body(...)):
    """
    Identify intervals of different heartrates of an exercise activity and return a JSON object.
    """
    untransformed_data = jsonable_encoder(request)
    activity = transform_to_previous_form(untransformed_data)
    Intervals = IntervalIdentificationByHeartRate(
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
    """
    Identify intervals of different heartrates of an exercise activity and return a .png chart render.
    """
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
    """
    Identify intervals of different power outputs of an exercise activity and return a JSON object.
    """
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
    """
    Identify intervals of different power outputs of an exercise activity and return a .png chart render.
    """
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

