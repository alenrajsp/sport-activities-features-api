import os
import uuid

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sport_activities_features import DataExtractionFromCSV

from helpers.file_reader import read_file
from models.models import FileModel

metadata = []

router = APIRouter(prefix="/csvreader",
                   tags=["CSV Reader"])


@router.post("/file/", response_class=JSONResponse)
async def all_activities_from_csv(file: UploadFile = File(...)):
    """
    Get all activities from a CSV file
    (based on collection sample)[https://github.com/firefly-cpp/sport-activities-features/blob/main/datasets/collection_sample.csv].
    """
    filename = str(uuid.uuid4())
    activities, data_extraction_from_csv = extract_csv(file, filename)
    return JSONResponse(content=jsonable_encoder(activities))


def extract_csv(file, filename):
    bytes = file.file.read()
    with open(f"temp/{filename}.csv", 'wb+') as file_obj:
        file_obj.write(bytes)
    data_extraction_from_csv = DataExtractionFromCSV()
    activities = data_extraction_from_csv.from_file(f"temp/{filename}.csv").to_json()
    os.remove(f"temp/{filename}.csv")
    return activities, data_extraction_from_csv


@router.post("/file/randomActivities", response_class=JSONResponse)
async def random_activities_from_csv(random_activities_count:int=3, file: UploadFile = File(...)):
    """ Get a random sample of activities from a CSV file
    (based on collection sample)[https://github.com/firefly-cpp/sport-activities-features/blob/main/datasets/collection_sample.csv]."""
    filename = str(uuid.uuid4())

    activities, data_extraction_from_csv = extract_csv(file, filename)
    random_activities = data_extraction_from_csv.select_random_activities(random_activities_count).to_json()

    return JSONResponse(content=jsonable_encoder(random_activities))