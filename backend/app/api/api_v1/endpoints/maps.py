import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder

from app.core.security import oauth2_scheme
from app.models.car import Car as ModelCar
from app.models.space import Space
from app.models.user import User as ModelUser
from app.models.zone import Zone


router = APIRouter(
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "This zone doesn't exist",
        }
    }
)


@router.get(
    "/",
    summary="Get the properties and objects of the global map of the parking lot.",
    responses={
        status.HTTP_200_OK: {
            "description": "A global map of the parking lot is returned successfully.",
            "content": {
                "application/json": {
                    "examples": {
                        "map": {
                            "summary": "map",
                            "value": {
                                "width": 0,
                                "height": 0,
                                "objects": [
                                    {
                                        "start": {
                                            "x": 10,
                                            "y": 10
                                        },
                                        "end": {
                                            "x": 30,
                                            "y": 50
                                        },
                                        "type": "zone",
                                        "id": 1,
                                        "name": "A",
                                        "free_spaces": 15,
                                        "own_booked_spaces": 0,
                                        "hourly_rate": 15
                                    },
                                ],
                            },
                        },
                    }
                },
            },
        },
    },
)
async def get_zones(auth_token: str = Depends(oauth2_scheme)):
    valid_email = await ModelUser.check_cookie(auth_token)
    if not valid_email:
        # user is not authorized
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    cars = await ModelCar.get_all(valid_email)
    zones = await Zone.get_zones()
    json_zones = []
    for zone in zones:
        json_zone = jsonable_encoder(zone)

        json_zone["type"] = "zone"

        start_x = json_zone.pop("start_x", None)
        start_y = json_zone.pop("start_y", None)
        json_zone["start"] = {"x": start_x, "y": start_y}

        end_x = json_zone.pop("end_x", None)
        end_y = json_zone.pop("end_y", None)
        json_zone["end"] = {"x": end_x, "y": end_y}
        zone_id = json_zone["id"]
        free_spaces = await Space.get_free_spaces(zone_id)
        json_zone["free_spaces"] = len(free_spaces)
        own_booked_spaces = 0
        for car in cars:
            curr_car = jsonable_encoder(car)
            curr_car_booked_spaces = await Space.get_own_booked_spaces(zone_id=zone_id, car_id=curr_car["id"])
            own_booked_spaces += len(curr_car_booked_spaces)
        if own_booked_spaces != 0:
            json_zone["own_booked_spaces"] = own_booked_spaces
        
        json_zones.append(json_zone)
    
    json_other = [
        {
            "type": "divider",
            "start": {
                "x": 1,
                "y": 66
            },
            "end": {
                "x": 98,
                "y": 66
            }
        },
        {
            "type": "divider",
            "start": {
                "x": 1,
                "y": 132
            },
            "end": {
                "x": 98,
                "y": 132
            }
        },
        {
            "type": "divider",
            "start": {
                "x": 114,
                "y": 66
            },
            "end": {
                "x": 210,
                "y": 66
            }
        },
        {
            "type": "divider",
            "start": {
                "x": 114,
                "y": 132
            },
            "end": {
                "x": 211,
                "y": 132
            }
        },
        {
            "type": "road",
            "start": {
                "x": 0,
                "y": 134
            },
            "end": {
                "x": 212,
                "y": 146
            }
        },
        {
            "type": "road",
            "start": {
                "x": 2,
                "y": 93
            },
            "end": {
                "x": 210,
                "y": 105
            }
        },
        {
            "type": "road",
            "start": {
                "x": 2,
                "y": 27
            },
            "end": {
                "x": 210,
                "y": 39
            }
        },
        {
            "type": "road",
            "start": {
                "x": 2,
                "y": 93
            },
            "end": {
                "x": 210,
                "y": 105
            }
        },
        {
            "type": "road",
            "start": {
                "x": 100,
                "y": 0
            },
            "end": {
                "x": 112,
                "y": 146
            }
        },
        {
            "type": "gate",
            "name": "1",
            "start": {
                "x": 100,
                "y": -1
            },
            "end": {
                "x": 112,
                "y": 1
            }
        },
        {
            "type": "gate",
            "name": "2",
            "start": {
                "x": -1,
                "y": 134
            },
            "end": {
                "x": 1,
                "y": 146
            }
        },
        {
            "type": "gate",
            "name": "3",
            "start": {
                "x": 211,
                "y": 134
            },
            "end": {
                "x": 213,
                "y": 146
            }
        }
    ]
    return {"width": 213, "height": 149, "objects": json_zones+json_other}
