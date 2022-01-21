import json
import os
from typing import List, Optional

import numpy as np
import overpy
from fastapi import APIRouter, File, UploadFile, HTTPException, Request, Body
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sport_activities_features import IntervalIdentificationByPower, IntervalIdentificationByHeartrate, PlotData
from sport_activities_features.area_identification import AreaIdentification
from sport_activities_features.overpy_node_manipulation import OverpyNodesReader
from sport_activities_features.tcx_manipulation import TCXFile
from sport_activities_features.gpx_manipulation import GPXFile
from sport_activities_features.weather_identification import WeatherIdentification
import uuid
import jsonpickle
from starlette.background import BackgroundTasks
from starlette.responses import JSONResponse
from fastapi.responses import FileResponse

from helpers.file_reader import read_file
from helpers.file_transformer import transform_to_previous_form
from helpers.overpy_transformer import OverpyNodeHelper
from helpers.temp_file import save_temp_plot_image
from models.models import FileModel, NodeModel, IntervalModel
import shutil

metadata = []


router = APIRouter(prefix="/area",
    tags=["Area identification"])


@router.post("/identification/", response_model=IntervalModel)
async def interval_identification_heartrate(files: List[UploadFile] = File(...)):
    uuid_folder_name = str(uuid.uuid4())
    folder_name = f'temp/{uuid_folder_name}/'
    os.mkdir(folder_name)
    areas = np.array([])

    for file in files:
        activity = read_file(file, file.filename)
        positions = np.array([*activity['positions']])
        distances = np.array([*activity['distances']])
        timestamps = np.array([*activity['timestamps']])
        heartrates = np.array([*activity['heartrates']])
        area_coordinates = np.array([[[47.530643, 15.706290], [47.570553, 15.744146], [47.554449, 15.789791],
                                      [47.534131, 15.751618], [47.543990, 15.735831], [47.524630, 15.742444]]])

        area = AreaIdentification(positions, distances, timestamps, heartrates, area_coordinates)
        area.identify_points_in_area()
        area_data = area.extract_data_in_area()
        if area_data['distance'] != 0.0:
            areas = np.append(areas, area)
        plot = area.plot_map()
        name = f'temp/{uuid_folder_name}/{file.filename}.png'
        plot.savefig(name)
    area_plot = AreaIdentification.plot_activities_inside_area_on_map(areas, area_coordinates)
    name = f'temp/{uuid_folder_name}/area.png'
    area_plot.savefig(name)

    shutil.make_archive(f'{uuid_folder_name}', 'zip', base_dir=f'temp/{uuid_folder_name}/', root_dir=f'temp/')

    data = {"test":"test"}

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
