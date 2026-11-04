from typing import Literal

from fastapi import APIRouter, Depends, Query, Response, status

from APP.security import get_current_user
from ..manager import employees as employee_manager
from ..schema.models import EmployeeCreate, EmployeeUpdate, StatusUpdate
from .responses import success_response

router = APIRouter(
    prefix="/employees",
    tags=["employees"],
    dependencies=[Depends(get_current_user)],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_employee_route(data: EmployeeCreate, response: Response) -> dict:
    employee = employee_manager.create_employee(data)
    return success_response(
        response,
        "Employee created successfully",
        employee,
        status.HTTP_201_CREATED,
    )


@router.get("/")
def get_all_employees_route(
    response: Response,
    department: str | None = None,
    employee_status: Literal["Active", "Inactive"] | None = Query(
        default=None, alias="status"
    ),
    search: str | None = None,
) -> dict:
    employees = employee_manager.get_all_employees(
        department,
        employee_status,
        search,
    )
    return success_response(response, "Employees retrieved successfully", employees)


@router.get("/{employee_id}")
def get_one_employee_route(employee_id: int, response: Response) -> dict:
    employee = employee_manager.get_one_employee(employee_id)
    return success_response(response, "Employee retrieved successfully", employee)


@router.put("/{employee_id}")
def replace_employee_route(
    employee_id: int,
    data: EmployeeCreate,
    response: Response,
) -> dict:
    employee = employee_manager.replace_employee(employee_id, data)
    return success_response(response, "Employee replaced successfully", employee)


@router.patch("/{employee_id}")
def update_employee_route(
    employee_id: int,
    data: EmployeeUpdate,
    response: Response,
) -> dict:
    employee = employee_manager.update_employee(employee_id, data)
    return success_response(response, "Employee updated successfully", employee)


@router.patch("/{employee_id}/status")
def update_employee_status_route(
    employee_id: int,
    data: StatusUpdate,
    response: Response,
) -> dict:
    employee = employee_manager.update_employee_status(employee_id, data)
    return success_response(response, "Employee status updated successfully", employee)


@router.delete("/{employee_id}")
def delete_employee_route(employee_id: int, response: Response) -> dict:
    employee_manager.delete_employee(employee_id)
    return success_response(
        response,
        "Employee deleted successfully",
        {"id": employee_id},
    )
