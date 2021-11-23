from pydantic import BaseModel


class User(BaseModel):
    email: str

    class Config:
        orm_mode = True

class LoginCode(BaseModel):
    login_code: str