import logging

from fastapi import Request
from redis.asyncio import Redis

from ..dto.driver_location_request import DriverLocationRequest
from ..dto.nearby_driver_response import NearbyDriverResponse

logger = logging.getLogger(__name__)
DRIVERS_GEO_KEY = "drivers:locations"



class LocationService:
    def __init__(self, redis : Redis ) -> None:
        self.redis = redis

    async def update_driver_location(self, location: DriverLocationRequest) -> None:
        await self.redis.geoadd(
            DRIVERS_GEO_KEY,
            (location.longitude, location.latitude, location.driver_id),
        )
        logger.info("Updated location for driver %s", location.driver_id)

    async def find_nearby_drivers(
        self, latitude: float, longitude: float, radius_km: float
    ) -> list[NearbyDriverResponse]:
        results = await self.redis.geosearch(
            DRIVERS_GEO_KEY,
            longitude=longitude,
            latitude=latitude,
            radius=radius_km,
            unit="km",
            sort="ASC",
            count=10,
            withdist=True,
            withcoord=True,
        )

        drivers = []
        for result in results:
            driver_id = result[0]
            distance_km = result[1]
            coordinates = result[2]

            driver = NearbyDriverResponse(
                driver_id=driver_id,
                latitude=coordinates[1],
                longitude=coordinates[0],
                distance_km=distance_km,
            )
            drivers.append(driver)

        logger.info("Found %d nearby drivers within %s km", len(drivers), radius_km)
        return drivers

    async def remove_driver(self, driver_id: str) -> None:
        await self.redis.zrem(DRIVERS_GEO_KEY, driver_id)
        logger.info("Removed driver %s from the location index", driver_id)






def get_location_service(request: Request) -> LocationService:
    return LocationService(request.app.state.redis_client)
