import os
import uuid

import numpy as np
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from sport_activities_features import HillIdentification, PlotData
from starlette.background import BackgroundTasks

from helpers.file_transformer import transform_to_previous_form
from helpers.temp_file import save_temp_plot_image
from models.models import FileModel

metadata = []

router = APIRouter(prefix="/hillIdentification",
                   tags=["Hill identification"])

@router.post("/image", response_class=FileResponse)
async def hill_identification(request: FileModel = Body(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    """
    Identify hills from the HillIdentification class and returns a png render of PlotData class as a file.
    """
    untransformed_data = jsonable_encoder(request)
    activity = transform_to_previous_form(untransformed_data)

    # Converting the read data to the array.
    altitudes = np.array([*activity['altitudes']])
    distances = np.array([*activity['distances']])

    Hill = HillIdentification(altitudes, 30)
    Hill.identify_hills()
    all_hills = Hill.return_hills()

    # draw detected hills
    Map = PlotData()

    plot = Map.plot_hills_on_map(altitudes, distances, all_hills)
    name, response = save_temp_plot_image(plot)
    background_tasks.add_task(os.remove, name)

    return response

