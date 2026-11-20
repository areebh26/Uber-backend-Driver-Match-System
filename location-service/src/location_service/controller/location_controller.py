from fastapi import APIRouter, Depends, Query, Request, status

from ..dto.driver_location_request import DriverLocationRequest
from ..dto.nearby_driver_response import NearbyDriverResponse
from ..service.location_service import get_location_service, LocationService

router = APIRouter(prefix="/api/v1/locations", tags=["locations"])





@router.post("/drivers/update", status_code=status.HTTP_200_OK)
async def update_driver_location(
    location: DriverLocationRequest,
    service: LocationService = Depends(get_location_service),
) :
    await service.update_driver_location(location)
    return {"message": "Driver location updated"}


@router.get("/drivers/nearby", status_code=status.HTTP_200_OK)
async def get_nearby_drivers(
    latitude: float = Query(),
    longitude: float = Query(),
    radius: float = Query(default=5.0),
    service: LocationService = Depends(get_location_service),
) -> list[NearbyDriverResponse]:
    return await service.find_nearby_drivers(latitude, longitude, radius)


@router.delete("/drivers/{driver_id}", status_code=status.HTTP_200_OK)
async def remove_driver(
    driver_id: str,
    service: LocationService = Depends(get_location_service),
) :
    await service.remove_driver(driver_id)
    return {"message": "Driver removed successfully"}
