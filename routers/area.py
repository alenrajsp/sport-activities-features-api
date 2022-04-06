import os
from typing import List
from zipfile import ZipFile
import os
import shutil
import uuid
from typing import List

import numpy as np
from fastapi import APIRouter, File, UploadFile, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from sport_activities_features import PlotData
from sport_activities_features.interval_identification import IntervalIdentificationByHeartRate, IntervalIdentificationByPower
from sport_activities_features.area_identification import AreaIdentification
from starlette.background import BackgroundTasks
from starlette.responses import JSONResponse

from helpers.file_reader import read_file
from helpers.file_transformer import transform_to_previous_form
from helpers.folder import Folder
from helpers.temp_file import save_temp_plot_image
from models.models import FileModel, IntervalModel

metadata = []

router = APIRouter(prefix="/area",
                   tags=["Area identification"])


@router.post("/identification/", response_class=FileResponse)
async def area_identification(files: List[UploadFile] = File(...),
                                            background_tasks: BackgroundTasks = BackgroundTasks()):
    uuid_folder_name = str(uuid.uuid4())
    folder_name = f'temp/{uuid_folder_name}/'
    os.mkdir(folder_name)
    areas = np.array([])

    folder_helper = Folder()
    zipObj = ZipFile(folder_helper.temp+os.path.sep+uuid_folder_name+'.zip', 'w')

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
        name = f'{folder_helper.temp}{os.path.sep}{uuid_folder_name}/{file.filename}.png'
        plot.savefig(name)
        zipObj.write(name, os.path.basename(name))

    area_plot = AreaIdentification.plot_activities_inside_area_on_map(areas, area_coordinates)
    name = f'{folder_helper.temp}{os.path.sep}{uuid_folder_name}{os.path.sep}area.png'

    area_plot.savefig(name)
    zipObj.write(name, os.path.basename(name))
    zipObj.close()
    shutil.rmtree(f'{folder_helper.temp}{os.path.sep}{uuid_folder_name}')


    response = FileResponse(folder_helper.temp+os.path.sep+uuid_folder_name+'.zip', media_type='application/octet-stream',
                            filename='area_identification_charts.zip')
    background_tasks.add_task(os.remove, folder_helper.temp+os.path.sep+uuid_folder_name+'.zip')

    return response
