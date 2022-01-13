from typing import List, Optional

from fastapi import APIRouter, File, UploadFile, HTTPException
from sport_activities_features.tcx_manipulation import TCXFile
from sport_activities_features.gpx_manipulation import GPXFile
import uuid
import jsonpickle
import os
from fastapi.encoders import jsonable_encoder
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from models.models import FileModel

metadata = []


router = APIRouter(prefix="/reader",
    tags=["reader"])

@router.post("/file/", response_model=FileModel)
async def read_file(file: UploadFile = File(...)):
    filename = str(uuid.uuid4())
    if file.filename.endswith('.gpx'):
        gpx_file = GPXFile()
        bytes = file.file.read()
        with open(f"temp/{filename}.gpx", 'wb+') as file_obj:
            file_obj.write(bytes)
        gpx = gpx_file.read_one_file(f"temp/{filename}.gpx")
        os.remove(f"temp/{filename}.gpx")
        return JSONResponse(content=jsonable_encoder(gpx))
    elif file.filename.endswith('.tcx'):
        tcx_file = TCXFile()
        tcx = tcx_file.read_one_file(file.file)
        return JSONResponse(content=jsonable_encoder(tcx))
    else:
        raise HTTPException(status_code=400, detail="File not of type .GPX / .TCX")


@router.post("/file/integralMetrics", response_model=FileModel)
async def read_file(file: UploadFile = File(...)):
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

