import uuid
import os

import numpy as np
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from sport_activities_features import HillIdentification, PlotData
from sport_activities_features.dead_end_identification import DeadEndIdentification
from starlette.background import BackgroundTasks

from helpers.file_transformer import transform_to_previous_form
from helpers.temp_file import save_temp_plot_image
from models.models import FileModel


metadata = []

router = APIRouter(prefix="/deadEndIdentification",
                   tags=["Dead-end identification"])



@router.post("/image", response_class=FileResponse)
async def identify_dead_ends(request: FileModel = Body(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    """
    Identify dead ends from the DeadEndIdentification() class and returns a png render as a file.
    """
    untransformed_data = jsonable_encoder(request)
    activity = transform_to_previous_form(untransformed_data)

    # Converting the read data to the array.
    positions = np.array([*activity['positions']])
    distances = np.array([*activity['distances']])

    # Identifying the dead ends.
    Dead_ends = DeadEndIdentification(positions, distances)
    Dead_ends.identify_dead_ends()
    plot = Dead_ends.show_map()

    name, response = save_temp_plot_image(plot)
    background_tasks.add_task(os.remove, name)

    return response


