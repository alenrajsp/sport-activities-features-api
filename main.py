from fastapi import FastAPI
from routers import reader, weather, overpy_node_manipulation, interval_identification, \
    banister_TRIMP, hill_identification, dead_end, missing_elevation, \
    topographic_features, interruptions, area
import uvicorn

import nest_asyncio
nest_asyncio.apply()

app = FastAPI(title="sport-activities-features API",
              description="FastAPI implementation of sport-activities-features for remote work.")


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

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=False, port=8000)
