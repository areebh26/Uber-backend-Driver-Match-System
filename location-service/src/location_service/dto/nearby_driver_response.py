from pydantic import BaseModel


class NearbyDriverResponse(BaseModel):
    driver_id: str
    latitude: float
    longitude: float
    distance_km: float
