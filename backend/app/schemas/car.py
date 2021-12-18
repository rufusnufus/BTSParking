from pydantic import BaseModel


class InputCar(BaseModel):
    model: str
    license_number: str

    class Config:
        orm_mode = True


class OutputCar(BaseModel):
    id: int
    model: str
    license_number: str


class Booking(BaseModel):
    occupying_car: OutputCar
    space_id: int
    booked_until: str

    class Config:
        orm_mode = True
