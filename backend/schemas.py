from enum import Enum
from pydantic import BaseModel, field_validator


class LanguageEnum(str, Enum):
    marathi = "mr"
    hindi = "hi"
    english = "en"


class UserRegister(BaseModel):
    full_name: str
    phone_number: str
    preferred_language: LanguageEnum = LanguageEnum.marathi
    password: str

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        if not value.isdigit():
            raise ValueError("Phone number must contain only digits")
        if len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits")
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return value


class UserLogin(BaseModel):
    phone_number: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"