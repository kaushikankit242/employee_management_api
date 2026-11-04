from typing import Literal

from ..exception import (
    DepartmentDoesNotExist,
    EmailAlreadyExists,
    EmployeeNotFound,
    NullUpdateField,
)
from ..schema.models import EmployeeCreate, EmployeeUpdate, StatusUpdate
from ..storage import repository


def create_employee(data: EmployeeCreate) -> dict:
    department = repository.find_department(data.department)
    if department is None:
        raise DepartmentDoesNotExist

    for employee in repository.list_employees():
        if employee["email"].lower() == data.email.lower():
            raise EmailAlreadyExists

    employee = data.model_dump()
    employee["department"] = department
    employee["id"] = repository.add_employee(employee)
    return employee


def get_all_employees(
    department: str | None = None,
    employee_status: Literal["Active", "Inactive"] | None = None,
    search: str | None = None,
) -> dict:
    results = repository.list_employees()

    if department:
        results = [
            employee for employee in results
            if employee["department"].lower() == department.lower()
        ]

    if employee_status:
        results = [
            employee for employee in results
            if employee["status"] == employee_status
        ]

    if search:
        term = search.strip().lower()
        results = [
            employee for employee in results
            if term in employee["name"].lower()
            or term in employee["email"].lower()
            or term in employee["designation"].lower()
        ]

    return {
        "total": len(results),
        "employees": results,
    }


def get_one_employee(employee_id: int) -> dict:
    employee = repository.get_employee(employee_id)
    if employee is None:
        raise EmployeeNotFound
    return employee


def replace_employee(employee_id: int, data: EmployeeCreate) -> dict:
    if repository.get_employee(employee_id) is None:
        raise EmployeeNotFound

    department = repository.find_department(data.department)
    if department is None:
        raise DepartmentDoesNotExist

    for other in repository.list_employees():
        if (
            other["id"] != employee_id
            and other["email"].lower() == data.email.lower()
        ):
            raise EmailAlreadyExists

    replacement = data.model_dump()
    replacement["department"] = department
    return repository.update_employee(employee_id, replacement)


def update_employee(employee_id: int, data: EmployeeUpdate) -> dict:
    if repository.get_employee(employee_id) is None:
        raise EmployeeNotFound

    changes = data.model_dump(exclude_unset=True)
    for field, value in changes.items():
        if value is None:
            raise NullUpdateField(field)

    if "department" in changes:
        department = repository.find_department(changes["department"])
        if department is None:
            raise DepartmentDoesNotExist
        changes["department"] = department

    if "email" in changes:
        for other in repository.list_employees():
            if (
                other["id"] != employee_id
                and other["email"].lower() == changes["email"].lower()
            ):
                raise EmailAlreadyExists

    return repository.update_employee(employee_id, changes)


def update_employee_status(employee_id: int, data: StatusUpdate) -> dict:
    if repository.get_employee(employee_id) is None:
        raise EmployeeNotFound
    return repository.update_employee(employee_id, {"status": data.status})


def delete_employee(employee_id: int) -> None:
    if repository.get_employee(employee_id) is None:
        raise EmployeeNotFound
    repository.remove_employee(employee_id)
