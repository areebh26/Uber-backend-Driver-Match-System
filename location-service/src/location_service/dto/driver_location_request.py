from pydantic import BaseModel

class DriverLocationRequest(BaseModel):
    driver_id: str
    latitude: float
    longitude: float