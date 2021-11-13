from fastapi import APIRouter

from ..routers import authorization, cars, zones

router = APIRouter(
    prefix="/api/v1",
)

router.include_router(authorization.router)
router.include_router(zones.router)
router.include_router(cars.router)
