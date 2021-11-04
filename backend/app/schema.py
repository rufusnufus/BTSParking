from pydantic import BaseModel

class User(BaseModel): 
    email: str

    class Config:
        orm_mode = True

class InputCar(BaseModel):
    model: str
    license_number: str

    class Config:
        orm_mode = True

class OutputCar(BaseModel):
    id: int
    model: str
    license_number: str


