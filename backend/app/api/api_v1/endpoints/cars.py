from typing import Optional

from fastapi import APIRouter, Body, Cookie, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder

from app.models.car import Car as ModelCar
from app.models.user import User as ModelUser
from app.schemas.car import InputCar, OutputCar

router = APIRouter()


@router.post(
    "/",
    summary="Create a new car",
    response_model=OutputCar,
    responses={
        status.HTTP_200_OK: {
            "description": "Car created successfully",
            "content": {
                "application/json": {
                    "examples": {
                        "touareg": {
                            "summary": "Volkswagen Touareg",
                            "value": {
                                "id": 1,
                                "model": "Volkswagen Touareg",
                                "license_number": "A000AA",
                            },
                        },
                    }
                }
            },
        },
    },
)
async def create_car(
    car: InputCar = Body(
        ...,
        examples={
            "touareg": {
                "summary": "Volkswagen Touareg",
                "value": {"model": "Volkswagen Touareg", "license_number": "A000AA"},
            },
        },
    ),
    AUTH_TOKEN: Optional[str] = Cookie(None),
):
    valid_email = await ModelUser.check_cookie(AUTH_TOKEN)
    if not valid_email:
        # user is not authorized
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    created_car = await ModelCar.create(**car.dict(), email=valid_email)
    return OutputCar(**created_car).dict()


@router.get(
    "/",
    summary="List the saved cars",
    responses={
        status.HTTP_200_OK: {
            "description": "Listing of all added cars of a user",
            "content": {
                "application/json": {
                    "examples": {
                        "cars": {
                            "summary": "cars",
                            "value": [
                                {
                                    "id": 1,
                                    "model": "Volkswagen Touareg",
                                    "license_number": "A000AA",
                                }
                            ],
                        },
                    }
                }
            },
        },
    },
)
async def get_cars(AUTH_TOKEN: Optional[str] = Cookie(None)):
    valid_email = await ModelUser.check_cookie(AUTH_TOKEN)
    if not valid_email:
        # user is not authorized
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    cars = await ModelCar.get_all(valid_email)
    json_cars = []
    for car in cars:
        json_car = jsonable_encoder(car)
        json_car.pop("email", None)
        json_cars.append(json_car)
    return json_cars


@router.delete(
    "/{car_id}",
    summary="Delete a saved car",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Car deleted successfully",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "This car isn't owned by this user",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "This car doesn't exist",
        },
    },
)
async def delete_car(car_id: int, AUTH_TOKEN: Optional[str] = Cookie(None)):
    valid_email = await ModelUser.check_cookie(AUTH_TOKEN)
    if not valid_email:
        # user is not authorized
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    car = await ModelCar.get(car_id)
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    deleted_car_id = await ModelCar.delete(car_id, valid_email)
    if deleted_car_id:
        assert deleted_car_id == car_id
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        # if user asks to get not his car
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


# @router.get("/{car_id}", response_model=OutputCar)
async def get_saved_car(car_id: int, AUTH_TOKEN: Optional[str] = Cookie(None)):
    valid_email = await ModelUser.check_cookie(AUTH_TOKEN)
    if not valid_email:
        # user is not authorized
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    car = await ModelCar.get(car_id, valid_email)
    if car:
        return OutputCar(**car).dict()
    else:
        # if user asks car that doesn't exist
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
