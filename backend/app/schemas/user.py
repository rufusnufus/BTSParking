from pydantic import BaseModel


class User(BaseModel):
    email: str

    class Config:
        orm_mode = True


class AuthData(BaseModel):
    login_code: str
