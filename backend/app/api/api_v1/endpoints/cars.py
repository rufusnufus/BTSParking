from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder

from app.core.security import cookie_is_none, oauth2_scheme
from app.logs import logger
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
    auth_token: str = Depends(oauth2_scheme),
):
    logger.info(f"function: create_car, params: car={car}")
    if cookie_is_none(auth_token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    valid_email = await ModelUser.check_cookie(auth_token)
    logger.info(f"function: create_car, email: {valid_email}")
    if not valid_email:
        # user is not authorized
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    logger.info(f"function: create_car, creating car for {valid_email}")
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
async def get_cars(auth_token: str = Depends(oauth2_scheme)):
    if cookie_is_none(auth_token):
        logger.info("function: get_cars, got cookie is None")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    valid_email = await ModelUser.check_cookie(auth_token)
    logger.info(f"function: get_cars, email: {valid_email}")
    if not valid_email:
        # user is not authorized
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    logger.info(f"function: get_cars, getting all {valid_email}'s cars")
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
async def delete_car(car_id: int, auth_token: str = Depends(oauth2_scheme)):
    logger.info(f"function: delete_car, params: car_id={car_id}")
    if cookie_is_none(auth_token):
        logger.info("function: delete_car, got cookie is None")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    valid_email = await ModelUser.check_cookie(auth_token)
    logger.info(f"function: delete_car, email: {valid_email}")
    if not valid_email:
        # user is not authorized
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    logger.info(f"function: delete_car, checking if car: {car_id} exists")
    car = await ModelCar.get(car_id)
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    logger.info(
        f"function: delete_car, deleting car: {car_id} if it is {valid_email}'s car"
    )
    deleted_car_id = await ModelCar.delete(car_id, valid_email)
    if deleted_car_id:
        assert deleted_car_id == car_id
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        # if user asks to get not his car
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
