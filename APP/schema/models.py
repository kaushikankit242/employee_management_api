from typing import Literal

from pydantic import BaseModel, Field


class EmployeeCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: str
    department: str
    designation: str
    salary: float = Field(gt=0)
    status: Literal["Active", "Inactive"] = "Active"


class EmployeeUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    email: str | None = None
    department: str | None = None
    designation: str | None = None
    salary: float | None = Field(default=None, gt=0)


class StatusUpdate(BaseModel):
    status: Literal["Active", "Inactive"]


class DepartmentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)


class DepartmentUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
