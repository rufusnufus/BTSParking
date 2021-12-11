import datetime

from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder

from app.core.security import cookie_is_none, oauth2_scheme
from app.logs import logger
from app.models.booking import Booking as ModelBooking
from app.models.car import Car as ModelCar
from app.models.road import Road
from app.models.space import Space
from app.models.user import User as ModelUser
from app.models.zone import Zone
from app.schemas.car import Booking

router = APIRouter(
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "This zone doesn't exist",
        }
    }
)


@router.get(
    "/{zone_id}/full-map",
    summary="Get the objects of the zone map and the information on occupants.",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "This zone doesn't exist.",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "A non-admin user attempted to access this endpoint.",
        },
        status.HTTP_200_OK: {
            "description": "A map of the zone with occupants is returned successfully",
            "content": {
                "application/json": {
                    "examples": {
                        "spaces": {
                            "summary": "spaces",
                            "value": {
                                "width": 97,
                                "height": 63,
                                "objects": [
                                    {
                                        "id": 1,
                                        "number": 1,
                                        "free": False,
                                        "type": "space",
                                        "start": {"x": 1, "y": 1},
                                        "end": {"x": 13, "y": 23},
                                        "booking": {
                                            "occupying_car": {
                                                "id": 2,
                                                "email": "rufusnufus@gmail.com",
                                                "model": "Volkswagen Touareg",
                                                "license_number": "A000AA",
                                            },
                                            "space_id": 1,
                                            "booked_from": "2021-11-27T14:44:10.765514",
                                            "booked_until": "2021-11-27T14:47:00",
                                        },
                                    },
                                    {
                                        "id": 2,
                                        "number": 2,
                                        "free": True,
                                        "type": "space",
                                        "start": {"x": 15, "y": 1},
                                        "end": {"x": 27, "y": 23},
                                    },
                                ],
                            },
                        },
                    },
                },
            },
        },
    },
)
async def get_spaces(zone_id: int, auth_token: str = Depends(oauth2_scheme)):
    logger.info(f"function: get_spaces, params: zone_id={zone_id}")

    if cookie_is_none(auth_token):
        logger.info(f"function: get_spaces, got cookie is None")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    valid_email = await ModelUser.check_cookie(auth_token)
    logger.info(f"function: get_spaces, email: {valid_email}")
    if not valid_email:
        # user is not authorized
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    logger.info(f"function: get_spaces, checking if {valid_email} is admin user")
    is_admin = await ModelUser.is_admin(valid_email)
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    logger.info(f"function: get_spaces, checking if zone: {zone_id} exists")
    zone = await Zone.get_zone(id=zone_id)
    if not zone:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    width, height = await Zone.get_width_height(id=zone_id)

    logger.info(f"function: get_spaces, getting all booked spaces")
    spaces = await Space.get_booked_spaces(zone_id)
    json_spaces = []
    for space in spaces:
        json_space = jsonable_encoder(space)

        json_space["free"] = False
        json_space["type"] = "space"

        json_space.pop("zone_id", None)
        car_id = json_space.pop("car_id", None)
        if car_id:
            occupying_car = await ModelCar.get(car_id)

        start_x = json_space.pop("start_x", None)
        start_y = json_space.pop("start_y", None)
        json_space["start"] = {"x": start_x, "y": start_y}

        end_x = json_space.pop("end_x", None)
        end_y = json_space.pop("end_y", None)
        json_space["end"] = {"x": end_x, "y": end_y}

        booked_from = json_space.pop("booked_from", None)
        booked_until = json_space.pop("booked_until", None)
        json_space["booking"] = {
            "occupying_car": occupying_car,
            "space_id": json_space["id"],
            "booked_from": booked_from,
            "booked_until": booked_until,
        }
        json_spaces.append(json_space)

    logger.info(f"function: get_spaces, getting all free spaces")
    free_spaces = await Space.get_free_spaces(zone_id)
    json_free_spaces = []
    for free_space in free_spaces:
        json_free_space = jsonable_encoder(free_space)

        json_free_space["free"] = True
        json_free_space["type"] = "space"

        json_free_space.pop("zone_id", None)
        json_free_space.pop("car_id", None)

        start_x = json_free_space.pop("start_x", None)
        start_y = json_free_space.pop("start_y", None)
        json_free_space["start"] = {"x": start_x, "y": start_y}

        end_x = json_free_space.pop("end_x", None)
        end_y = json_free_space.pop("end_y", None)
        json_free_space["end"] = {"x": end_x, "y": end_y}

        json_free_space.pop("booked_from", None)
        json_free_space.pop("booked_until", None)

        json_free_spaces.append(json_free_space)

    logger.info(f"function: get_spaces, getting all roads in zone: {zone_id}")
    roads = await Road.get_roads(zone_id)
    json_roads = []
    for road in roads:
        json_road = jsonable_encoder(road)

        json_road["type"] = "road"

        json_road.pop("zone_id", None)
        json_road.pop("id", None)

        start_x = json_road.pop("start_x", None)
        start_y = json_road.pop("start_y", None)
        json_road["start"] = {"x": start_x, "y": start_y}

        end_x = json_road.pop("end_x", None)
        end_y = json_road.pop("end_y", None)
        json_road["end"] = {"x": end_x, "y": end_y}

        json_roads.append(json_road)
    return {
        "width": width,
        "height": height,
        "objects": json_spaces + json_free_spaces + json_roads,
    }


@router.get(
    "/{zone_id}/map",
    summary="Get the objects of the zone map and information on own cars.",
    responses={
        status.HTTP_200_OK: {
            "description": """A map of the zone with user's
                                own cars is returned successfully.""",
            "content": {
                "application/json": {
                    "examples": {
                        "free-spaces": {
                            "summary": "free-spaces",
                            "value": {
                                "width": 97,
                                "height": 63,
                                "objects": [
                                    {
                                        "id": 1,
                                        "number": 1,
                                        "free": False,
                                        "type": "space",
                                        "start": {"x": 1, "y": 1},
                                        "end": {"x": 13, "y": 23},
                                        "booking": {
                                            "occupying_car": {
                                                "id": 1,
                                                "email": "example@gmail.com",
                                                "model": "Volkswagen Touareg",
                                                "license_number": "A000AA",
                                            },
                                            "space_id": 1,
                                            "booked_from": "2021-11-27T14:34:44.529553",
                                            "booked_until": "2021-11-27T14:36:00",
                                        },
                                    },
                                ],
                            },
                        },
                    }
                }
            },
        },
    },
)
async def get_own_spaces(zone_id: int, auth_token: str = Depends(oauth2_scheme)):
    logger.info(f"function: get_own_spaces, params: zone_id={zone_id}")

    if cookie_is_none(auth_token):
        logger.info(f"function: get_own_spaces, got cookie is None")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    valid_email = await ModelUser.check_cookie(auth_token)
    logger.info(f"function: get_own_spaces, email: {valid_email}")
    if not valid_email:
        # user is not authorized
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    logger.info(f"function: get_own_spaces, checking if zone: {zone_id} exists")
    zone = await Zone.get_zone(id=zone_id)
    if not zone:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    width, height = await Zone.get_width_height(id=zone_id)

    cars = await ModelCar.get_all(valid_email)
    own_booked_spaces = []
    for car in cars:
        curr_car = jsonable_encoder(car)
        curr_car_booked_spaces = await Space.get_own_booked_spaces(
            zone_id=zone_id, car_id=curr_car["id"]
        )
        for booked_space in curr_car_booked_spaces:
            json_booked_space = jsonable_encoder(booked_space)
            json_booked_space["free"] = False
            json_booked_space["type"] = "space"

            json_booked_space.pop("zone_id", None)
            car_id = json_booked_space.pop("car_id", None)
            if car_id:
                occupying_car = await ModelCar.get(car_id)

            start_x = json_booked_space.pop("start_x", None)
            start_y = json_booked_space.pop("start_y", None)
            json_booked_space["start"] = {"x": start_x, "y": start_y}

            end_x = json_booked_space.pop("end_x", None)
            end_y = json_booked_space.pop("end_y", None)
            json_booked_space["end"] = {"x": end_x, "y": end_y}

            booked_from = json_booked_space.pop("booked_from", None)
            booked_until = json_booked_space.pop("booked_until", None)
            json_booked_space["booking"] = {
                "occupying_car": occupying_car,
                "space_id": json_booked_space["id"],
                "booked_from": booked_from,
                "booked_until": booked_until,
            }
            own_booked_spaces.append(json_booked_space)
    return {"width": width, "height": height, "objects": own_booked_spaces}


@router.post(
    "/{zone_id}/book",
    summary="Book a parking space",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Space booked successfully",
        },
        status.HTTP_306_RESERVED: {
            "description": "This space is occupied.",
        },
    },
)
async def book_space(
    zone_id: int,
    space: Booking = Body(
        ...,
        examples={
            "booking_example": {
                "summary": "booking_example",
                "value": {
                    "occupying_car": {
                        "id": 1,
                        "model": "Volkswagen Touareg",
                        "license_number": "A000AA",
                    },
                    "space_id": 3,
                    "booked_from": "2021-11-01T18:00Z",
                    "booked_until": "2021-11-01T20:00Z",
                },
            }
        },
    ),
    auth_token: str = Depends(oauth2_scheme),
):
    logger.info(
        f"function: book_space, params: zone_id={zone_id}, space={space}"
    )
    if cookie_is_none(auth_token):
        logger.info(f"function: book_space, got cookie is None")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    valid_email = await ModelUser.check_cookie(auth_token)
    logger.info(f"function: book_space, email: {valid_email}")
    if not valid_email:
        # user is not authorized
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    logger.info(f"function: book_space, checking if zone: {zone_id} exists")
    zone = await Zone.get_zone(zone_id)
    if not zone:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    free_space = await Space.check_free_space(space.space_id, zone_id)
    if not free_space:
        return Response(status_code=status.HTTP_306_RESERVED)

    booked_from = datetime.datetime.now()
    booked_until = datetime.datetime.strptime(space.booked_until, "%Y-%m-%dT%H:%MZ")
    logger.info(f"function: book_space, booked_until={type(booked_from)}")

    user_booking = await ModelBooking.add_booking(
        booked_from=booked_from,
        booked_until=booked_until,
        space_id=space.space_id,
        car_id=space.occupying_car.id,
        email=valid_email,
    )
    if not user_booking:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    booked_space = await Space.book_space(
        car_id=space.occupying_car.id,
        space_id=space.space_id,
        zone_id=zone_id,
        booked_from=booked_from,
        booked_until=booked_until,
    )

    if booked_space:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
