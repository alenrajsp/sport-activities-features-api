import json
from typing import List, Optional

import overpy
from fastapi import APIRouter, File, UploadFile, HTTPException, Request, Body
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sport_activities_features.overpy_node_manipulation import OverpyNodesReader
from sport_activities_features.tcx_manipulation import TCXFile
from sport_activities_features.gpx_manipulation import GPXFile
from sport_activities_features.weather_identification import WeatherIdentification
import uuid
import jsonpickle
from starlette.responses import JSONResponse

from helpers.file_transformer import transform_to_previous_form
from helpers.overpy_transformer import OverpyNodeHelper
from models.models import FileModel, NodeModel

metadata = []


router = APIRouter(prefix="/overpy",
    tags=["overpy"])


@router.post("/generate/", response_model=FileModel)
async def identify_nodes(request: List[NodeModel] = Body(...)):
    overpy_nodes = []
    json_request = jsonable_encoder(request)
    for node in json_request:
        op_node = OverpyNodeHelper(data=node)
        overpy_nodes.append(overpy.Node.from_json(data=op_node))
    overpy_reader = OverpyNodesReader(open_elevation_api="https://api.open-elevation.com/api/v1/lookup")
    # Returns {
    #         'positions': positions, 'altitudes': altitudes, 'distances': distances, 'total_distance': total_distance
    #         }
    data = overpy_reader.read_nodes(overpy_nodes)

    return JSONResponse(content=jsonable_encoder(data))

