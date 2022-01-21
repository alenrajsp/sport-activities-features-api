from typing import Optional, List

from pydantic import BaseModel


class FileModel(BaseModel):
    activity_type: Optional[str] = None
    positions: List[List[float]] = []
    altitudes: List[float] = []
    distances: List[float] = []
    total_distance: float = 0
    timestamps: List[str] = []
    heartrates: Optional[List[Optional[int]]] = None
    speeds: List[float] = []
    weather: Optional[List[dict]] = []


class AltitudeModel(BaseModel):
    altitudes: List[float] = []


class HillDataModel(BaseModel):
    number_of_hills: int
    average_altitude: float
    average_ascent: float
    total_distance: float
    total_distance_hills: float
    hills_share: float


class NodeModel(BaseModel):
    attributes: Optional[dict] = []
    id: int
    lat: float = 0
    lon: float = 0
    tags: Optional[dict] = []


class IntervalModel(BaseModel):
    intervals: List[List[int]]
    statistics: dict


class BannisterTRIPMModel(BaseModel):
    TRIPM: int
