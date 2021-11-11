from fastapi import APIRouter, HTTPException, status, Response, Cookie, Body
from fastapi.encoders import jsonable_encoder
from typing import Optional
from ..models import Car as ModelCar, User as ModelUser
from ..schema import InputCar, OutputCar
from ..responses import create_car_responses, get_cars_responses, delete_car_responses
from ..examples import car_example


router = APIRouter(
    prefix="/cars",
    tags=["Car Management"],
    responses={status.HTTP_401_UNAUTHORIZED: {"description": "The request is not authorized"}},
)


@router.post("/", summary="Create a new car", response_model=OutputCar, responses=create_car_responses)
async def create_car(car: InputCar = Body(..., examples= car_example), AUTH_TOKEN: Optional[str] = Cookie(None)):
    valid_email = await ModelUser.check_cookie(AUTH_TOKEN)
    if not valid_email: 
        # user is not authorized
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No authorization cookie is provided")
    created_car = await ModelCar.create(**car.dict(), email=valid_email)
    return OutputCar(**created_car).dict()

@router.get("/", summary="List the saved cars", responses=get_cars_responses)
async def get_cars(AUTH_TOKEN: Optional[str] = Cookie(None)):
    valid_email = await ModelUser.check_cookie(AUTH_TOKEN)
    if not valid_email: 
        # user is not authorized
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No authorization cookie is provided")
    cars = await ModelCar.get_all(valid_email)
    json_cars=[]
    for car in cars:
        json_car = jsonable_encoder(car)
        json_car.pop('email', None)
        json_cars.append(json_car)
    # return Response(status_code=status.HTTP_200_OK, content=json_cars)
    return json_cars

@router.delete("/{car_id}", summary="Delete a saved car", status_code=status.HTTP_204_NO_CONTENT, responses=delete_car_responses)
async def delete_car(car_id: int, AUTH_TOKEN: Optional[str] = Cookie(None)):
    valid_email = await ModelUser.check_cookie(AUTH_TOKEN)
    if not valid_email: 
        # user is not authorized
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No authorization cookie is provided")
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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No authorization cookie is provided")
    car = await ModelCar.get(car_id, valid_email)
    if car: 
        return OutputCar(**car).dict()
    else:
        # if user asks car that doesn't exist
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
