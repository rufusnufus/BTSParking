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
