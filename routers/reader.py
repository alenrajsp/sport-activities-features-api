import os
import uuid

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sport_activities_features.gpx_manipulation import GPXFile
from sport_activities_features.tcx_manipulation import TCXFile

from helpers.file_reader import read_file
from models.models import FileModel, IntegralMetricsModel

metadata = []

router = APIRouter(prefix="/reader",
                   tags=["Reader"])


@router.post("/file/", response_model=FileModel)
async def transform_file(file: UploadFile = File(..., description="GPX or TCX file")):
    """
    Process a TCX/GPX file into a **JSON** object.
    """
    filename = str(uuid.uuid4())
    file = read_file(file, filename)

    if (file == None):
        raise HTTPException(status_code=400, detail="File not of type .GPX / .TCX")

    return JSONResponse(content=jsonable_encoder(file))


@router.post("/file/integralMetrics", response_model=IntegralMetricsModel)
async def extract_integral_metrics(file: UploadFile = File(...,
                                                           description="GPX or TCX file")):
    """
    Extract integral metrics of the GPX/TCX file.
    """
    filename = str(uuid.uuid4())
    if file.filename.endswith('.gpx'):
        gpx_file = GPXFile()
        bytes = file.file.read()
        with open(f"temp/{filename}.gpx", 'wb+') as file_obj:
            file_obj.write(bytes)
        gpx = gpx_file.extract_integral_metrics(f"temp/{filename}.gpx")
        os.remove(f"temp/{filename}.gpx")
        return JSONResponse(content=jsonable_encoder(gpx))
    elif file.filename.endswith('.tcx'):
        tcx_file = TCXFile()
        tcx = tcx_file.extract_integral_metrics(file.file)
        return JSONResponse(content=jsonable_encoder(tcx))
    else:
        raise HTTPException(status_code=400, detail="File not of type .GPX / .TCX")
