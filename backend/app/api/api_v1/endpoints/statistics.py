from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder

from app.core.security import cookie_is_none, oauth2_scheme
from app.models.car import Car as ModelCar
from app.models.booking import Booking
from app.models.space import Space
from app.models.zone import Zone
from app.models.user import User as ModelUser

router = APIRouter()

@router.get(
    "/",
    summary="Get the whole information of user bookings.",
    responses={
        status.HTTP_200_OK: {
            "description": "A global map of the parking lot is returned successfully.",
            "content": {
                "application/json": {
                    "examples": {
                        "statistics": {
                            "summary": "statistics",
                            "value": [{
                                "hourly_rate": 15,
                                "booking": {
                                    "occupying_car": {
                                        "id": 1,
                                        "model": "Volkswagen Touareg",
                                        "license_number": "A000AA"
                                    },
                                    "space_id": 3,
                                    "booked_from": "2021-11-01T18:00Z",
                                    "booked_until": "2021-11-01T20:00Z"
                                }
                            }],
                        },
                    }
                }
            },
        },
    },
)
async def get_statistics(
    auth_token: str = Depends(oauth2_scheme),
):
    if cookie_is_none(auth_token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    valid_email = await ModelUser.check_cookie(auth_token)
    if not valid_email:
        # user is not authorized
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    bookings = await Booking.get_bookings(valid_email)
    own_bookings = []
    for booking in bookings:
        json_booking = jsonable_encoder(booking)
        occupying_car = await ModelCar.get(json_booking["car_id"])
        occupying_car = jsonable_encoder(occupying_car)
        occupying_car.pop("email", None)
        zone = await Space.get_zone_by_space(json_booking["space_id"])
        hourly_rate = await Zone.get_hourly_rate_by_zone(zone)
        json_booking["hourly_rate"] = hourly_rate
        json_booking["booking"] = {
                "occupying_car": occupying_car,
                "space_id": json_booking["space_id"],
                "booked_from": json_booking["booked_from"].split('.')[0],
                "booked_until": json_booking["booked_until"],
            }
        json_booking.pop("car_id", None)
        json_booking.pop("space_id", None)
        json_booking.pop("booked_from", None)
        json_booking.pop("booked_until", None)
        own_bookings.append(json_booking)
    return own_bookings
