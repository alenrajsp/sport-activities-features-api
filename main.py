import uvicorn
from fastapi import FastAPI

from routers import reader, weather, overpy_node_manipulation, interval_identification, \
    banister_TRIMP, hill_identification, dead_end, missing_elevation, \
    topographic_features, interruptions, area, csv


title = "sport-activities-features API"
description = """
FastAPI implementation of [sport-activities-features](https://github.com/firefly-cpp/sport-activities-features).
All the response files are of either a **JSON**, **.png** or **.zip** format.

Possible operations implemented from the non API version include:

### TCXFile/GPXFile
* Read **TCX** and **GPX** files and receive **JSON** representations of the read files.
* Extract integral metrics of the sports exercise

### WeatherIdentification
* Extract historical weather data for the parsed exercise using an outside dependency
[Visual Crossing](https://visualcrossing.com/), from JSON processed exercise. **API key is required**.

### ElevationIdentification
* Identify elevation data (in meters) of TCX/GPX training record processed JSON exercise using the
[Open-Elevation API](https://open-elevation.com/). If a lot of requests are to be made a 
[self-hosted](https://open-elevation.com/#host-your-own) API is prefferable.

### BanisterTRIMP -> 
* Calculate Bannister Training Impulse from duration and average heartrate.

### OverpyNodesReader
* Transform Overpy.node JSON objects into exercise like JSON files. [Open-Elevation API](https://open-elevation.com/).
is required.

### DeadEndIdentification
* Identify dead ends from a TCX or GPX file and return a .png render.

### HillIdentification
* Identify hills from the HillIdentification class and return a png render.

### InterruptionProcessor
* Identify interruptions (sudden stoppages) and the nature of them (currently if they happened near intersections).

### IntervalIdentificationByPower and IntervalIdentificationByHeartrate
* Identify intervals in the activity by heartrate or power
* Generate .png charts of heartrate and power intervals

### TopographicFeatures
* Identify number of hills, average altitude, average ascent, distance of the hills and a percentage of hills
in an JSON processed exercise.

### DataExtractionFromCSV
* Extract activity data from CSV files.

### AreaIdentification
* Identify activities inside a given polygon area and render them on a png generated map.

"""
version = "0.1.0"
app = FastAPI(title=title, description=description, version=version)

app.include_router(reader.router)
app.include_router(weather.router)
app.include_router(overpy_node_manipulation.router)
app.include_router(interval_identification.router)
app.include_router(banister_TRIMP.router)
app.include_router(hill_identification.router)
app.include_router(interval_identification.router)
app.include_router(dead_end.router)
app.include_router(missing_elevation.router)
app.include_router(topographic_features.router)
app.include_router(interruptions.router)
app.include_router(area.router)
app.include_router(csv.router)


@app.get("/")
async def root():
    return {"message": "Server works!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=False, port=8000)
