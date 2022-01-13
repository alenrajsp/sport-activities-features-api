import numpy as np
from fastapi import APIRouter, File, UploadFile, HTTPException, Body
from sport_activities_features import TCXFile
from sport_activities_features.dead_end_identification import DeadEndIdentification
from sport_activities_features.training_loads import BanisterTRIMP
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from helpers.file_transformer import transform_to_previous_form
from models.models import FileModel

metadata = []


router = APIRouter(prefix="/deadEndIdentification",
    tags=["Dead end identification"])

@router.post("/", response_model=FileModel)
async def identify_dead_ends(request: FileModel = Body(...)):
    """
    TO-DO: Does not work in original library!!!
    :param request:
    :return:
    """
    untransformed_data = jsonable_encoder(request)
    activity = transform_to_previous_form(untransformed_data)

    # Converting the read data to the array.
    positions = np.array([*activity['positions']])
    distances = np.array([*activity['distances']])

    # Identifying the dead ends.
    Dead_ends = DeadEndIdentification(positions, distances)
    Dead_ends.identify_dead_ends()
    Dead_ends.draw_map()

    return JSONResponse(content=jsonable_encoder(activity))





