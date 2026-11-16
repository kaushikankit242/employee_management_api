
import re

from pydantic import BaseModel, Field, field_validator

_EMAIL_PATTERN = re.compile(
    r"[A-Za-z0-9_%+-]+(?:\.[A-Za-z0-9_%+-]+)*@"
    r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?\.)+"
    r"[A-Za-z]{2,}"
)


def validate_email_address(value: str) -> str:
    if not _EMAIL_PATTERN.fullmatch(value):
        raise ValueError(
            "Invalid email address. Use the format name@example.com."
        )
    return value


class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str
    password: str = Field(min_length=8)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        return validate_email_address(value)


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    username: str
    email: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        return validate_email_address(value)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
