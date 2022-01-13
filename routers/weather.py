from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from sport_activities_features.weather_identification import WeatherIdentification
from starlette.responses import JSONResponse

from helpers.file_transformer import transform_to_previous_form
from models.models import FileModel

metadata = []


router = APIRouter(prefix="/weather",
    tags=["weather"])


@router.post("/identification/", response_model=FileModel)
async def identify_weather(vc_api_key: str, request: FileModel = Body(...)):
    """
    REQUEST

        POST /weather/identification/

        Body: Response of JSON /reader/

    RESPONSE

        JSON with added Weather data
    """
    untransformed_data = jsonable_encoder(request)
    standardized_data = transform_to_previous_form(untransformed_data)
    weather_identificator = WeatherIdentification(standardized_data['positions'], standardized_data['timestamps'], vc_api_key=vc_api_key)
    weather = weather_identificator.get_weather()
    standardized_data.update({'weather':weather})
    return JSONResponse(content=jsonable_encoder(standardized_data))

