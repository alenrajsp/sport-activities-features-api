from fastapi import FastAPI
from routers import reader, weather,overpy_node_manipulation,interval_identification, banister_TRIMP, dead_end_identification
import uvicorn

app = FastAPI()

app.include_router(reader.router)
app.include_router(weather.router)
app.include_router(overpy_node_manipulation.router)
app.include_router(interval_identification.router)
app.include_router(banister_TRIMP.router)
app.include_router(dead_end_identification.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=False, port=8000)
