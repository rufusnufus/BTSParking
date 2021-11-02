from typing import List

import uvicorn
from app.models import Car as ModelCar
from app.schema import InputCar, OutputCar
from app.app import app
from fastapi import status, Response
from app.db import db

@app.post("/cars/")
async def create_car(car: InputCar):
    car_id = await ModelCar.create(**car.dict())
    return {"id": car_id}

@app.get("/cars/", response_model=List[OutputCar])
async def get_cars():
    cars = await ModelCar.get_all()
    return cars

@app.delete("/cars/{carID}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_car(carID: int):
    car_id = await ModelCar.delete(carID)
    assert car_id == carID
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get("/cars/{carID}", response_model=OutputCar)
async def get_car(carID: int):
    car = await ModelCar.get(carID)
    return OutputCar(**car).dict()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
