from fastapi import APIRouter, status

from app.api.api_v1.endpoints import authorization, cars, maps, zones

router = APIRouter(
    prefix="/api/v1",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "The request is not authorized"}
    },
)

router.include_router(authorization.router, tags=["Authorization"])
router.include_router(maps.router, prefix="/map", tags=["Booking"])
router.include_router(zones.router, prefix="/zones", tags=["Booking"])
router.include_router(cars.router, prefix="/cars", tags=["Car Management"])
