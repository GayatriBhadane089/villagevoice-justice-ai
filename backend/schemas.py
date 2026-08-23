from pydantic import BaseModel


class UserRegister(BaseModel):
    full_name: str
    phone_number: str
    preferred_language: str = "mr"
    password: str


class UserLogin(BaseModel):
    phone_number: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"