# sport-activities-features API

Sport-activities-features API is a Python library for using 
[sport-activities-features](https://github.com/firefly-cpp/sport-activities-features) as an FastAPI based web API.

### Note
Please view [Swagger docs](localhost:8000/docs) to see how to use this API.

## Installation

1. Download project
2. Install dependencies with Poetry
```bash
poetry install
```
3. Navigate to project folder and run server in terminal.
```bash
uvicorn main:app --reload
```

## How to use (locally)
1. Run server (**main.py**)
2. Navigate to [Swagger docs](localhost:8000/docs) to see how to use.


## How to use (Docker)
1. Use the official image from DockerHub repository 
   (alenrajsp/sport-activities-features-api:0.2)[https://hub.docker.com/r/alenrajsp/sport-activities-features-api]
2. Run from terminal with 
   `docker run -p <PORT>:80 alenrajsp/niaamlapi:0.2`. 
   The **\<PORT>** variable is the port from which you want to access the container.

| Folder / file      | Description |
| ----------- | ----------- |
| /helpers      | Folder for helper classes (JSON transformations, folder navigation, temp file management)       |
| /models   | Request / Response FastAPI models        |
| /routers   | Individual routes of FastAPI and functionalities        |
| /temp   | Temporary files that, get generated when recieving requests and deleted afterwards     |



## License
[MIT](https://choosealicense.com/licenses/mit/)