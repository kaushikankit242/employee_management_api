from typing import Literal

from pydantic import BaseModel, Field, field_validator

from .auth import validate_email_address


class EmployeeCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: str
    department: str
    designation: str
    salary: float = Field(gt=0)
    status: Literal["Active", "Inactive"] = "Active"

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        return validate_email_address(value)


class EmployeeUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    email: str | None = None
    department: str | None = None
    designation: str | None = None
    salary: float | None = Field(default=None, gt=0)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str | None) -> str | None:
        return validate_email_address(value) if value is not None else None


class StatusUpdate(BaseModel):
    status: Literal["Active", "Inactive"]


class DepartmentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)


class DepartmentUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=100)


class EmployeeResponse(EmployeeCreate):
    id: int

    model_config = {"from_attributes": True}


class DepartmentResponse(DepartmentCreate):
    id: int

    model_config = {"from_attributes": True}
