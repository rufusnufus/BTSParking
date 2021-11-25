from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder

from app.core.security import cookie_is_none, oauth2_scheme
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
    summary="List all zones in a parking lot",
)
async def get_zones():
    # if cookie_is_none(auth_token):
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # valid_email = await ModelUser.check_cookie(auth_token)
    # if not valid_email:
    #     # user is not authorized
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    zones = await Zone.get_zones()
    json_zones = []
    for zone in zones:
        json_zone = jsonable_encoder(zone)

        start_x = json_zone.pop("start_x", None)
        start_y = json_zone.pop("start_y", None)
        json_zone["start"] = {"x": start_x, "y": start_y}

        end_x = json_zone.pop("end_x", None)
        end_y = json_zone.pop("end_y", None)
        json_zone["end"] = {"x": end_x, "y": end_y}

        json_zones.append(json_zone)
    return json_zones


@router.get(
    "/{zone_id}/spaces",
    summary="List all the spaces in the zone along with the current occupying vehicles",
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "A non-admin user attempted to access this endpoint.",
        },
        status.HTTP_200_OK: {
            "description": "A listing of parking spaces is obtained successfully.",
            "content": {
                "application/json": {
                    "examples": {
                        "spaces": {
                            "summary": "spaces",
                            "value": [
                                {
                                    "id": 2,
                                    "number": 2,
                                    "start": {"x": 40, "y": 0},
                                    "end": {"x": 80, "y": 40},
                                },
                                {
                                    "id": 1,
                                    "number": 1,
                                    "occupying_car_id": 1,
                                    "start": {"x": 0, "y": 0},
                                    "end": {"x": 40, "y": 40},
                                },
                            ],
                        },
                    }
                }
            },
        },
    },
)
async def get_spaces(zone_id: int, auth_token: str = Depends(oauth2_scheme)):
    if cookie_is_none(auth_token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    valid_email = await ModelUser.check_cookie(auth_token)
    if not valid_email:
        # user is not authorized
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    is_admin = await ModelUser.is_admin(valid_email)
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    # TODO: create zone validation for 404 error, when zones table will be ready

    spaces = await Space.get_spaces(zone_id)
    json_spaces = []
    for space in spaces:
        json_space = jsonable_encoder(space)

        json_space.pop("zone_id", None)
        car_id = json_space.pop("car_id", None)
        if car_id:
            json_space["occupying_car_id"] = car_id

        start_x = json_space.pop("start_x", None)
        start_y = json_space.pop("start_y", None)
        json_space["start"] = {"x": start_x, "y": start_y}

        end_x = json_space.pop("end_x", None)
        end_y = json_space.pop("end_y", None)
        json_space["end"] = {"x": end_x, "y": end_y}

        json_spaces.append(json_space)
    return json_spaces


@router.get(
    "/{zone_id}/free-spaces",
    summary="List the spaces that are available for parking",
    responses={
        status.HTTP_200_OK: {
            "description": """A listing of available parking spaces
                                is obtained successfully""",
            "content": {
                "application/json": {
                    "examples": {
                        "free-spaces": {
                            "summary": "free-spaces",
                            "value": [
                                {
                                    "id": 1,
                                    "number": 1,
                                    "start": {"x": 0, "y": 0},
                                    "end": {"x": 40, "y": 40},
                                }
                            ],
                        },
                    }
                }
            },
        },
    },
)
async def get_free_spaces(zone_id: int):
    # if cookie_is_none(auth_token):
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # valid_email = await ModelUser.check_cookie(auth_token)
    # if not valid_email:
    #     # user is not authorized
    #     raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    free_spaces = await Space.get_free_spaces(zone_id)
    json_free_spaces = []
    for free_space in free_spaces:
        json_free_space = jsonable_encoder(free_space)

        json_free_space.pop("zone_id", None)
        json_free_space.pop("car_id", None)

        start_x = json_free_space.pop("start_x", None)
        start_y = json_free_space.pop("start_y", None)
        json_free_space["start"] = {"x": start_x, "y": start_y}

        end_x = json_free_space.pop("end_x", None)
        end_y = json_free_space.pop("end_y", None)
        json_free_space["end"] = {"x": end_x, "y": end_y}

        json_free_spaces.append(json_free_space)
    return json_free_spaces


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
    space_id: int = Body(..., embed=True),
    car_id: int = Body(..., embed=True),
    auth_token: str = Depends(oauth2_scheme),
):
    if cookie_is_none(auth_token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    valid_email = await ModelUser.check_cookie(auth_token)
    if not valid_email:
        # user is not authorized
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    zone = await Zone.get_zone(zone_id)
    if not zone:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    free_space = await Space.check_free_space(space_id, zone_id)
    if not free_space:
        return Response(status_code=status.HTTP_306_RESERVED)

    booked_space = await Space.book_space(
        car_id=car_id, space_id=space_id, zone_id=zone_id
    )

    if booked_space:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post(
    "/{zone_id}/release",
    summary="Stop occupying a parking space",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Parking space released successfully.",
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "This place isn't booked.",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "This place is booked by another user.",
        },
    },
)
async def book_release(
    zone_id: int,
    space_id: int = Body(..., embed=True),
    auth_token: str = Depends(oauth2_scheme),
):
    if cookie_is_none(auth_token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    valid_email = await ModelUser.check_cookie(auth_token)
    if not valid_email:
        # user is not authorized
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    free_space = await Space.check_free_space(space_id, zone_id)
    if free_space:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    # check whether user has his car on space which tries to release
    space = await Space.get_space(space_id, zone_id)
    if not space:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # check whether user has his car on space which tries to release
    user_car = await ModelCar.get(dict(space)["car_id"], valid_email)
    if not user_car:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    freed_space = await Space.release_space(space_id, zone_id)
    if freed_space:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
