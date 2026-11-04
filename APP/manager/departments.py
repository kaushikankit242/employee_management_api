from ..exception import (
    DepartmentAlreadyExists,
    DepartmentHasEmployees,
    DepartmentNotFound,
)
from ..schema.models import DepartmentCreate, DepartmentUpdate
from ..storage import repository


def create_department(data: DepartmentCreate) -> dict[str, int | str]:
    if repository.find_department(data.name):
        raise DepartmentAlreadyExists

    department_name = data.name.strip()
    department_id = repository.add_department(department_name)
    return {
        "id": department_id,
        "name": department_name,
    }


def get_departments() -> list[dict[str, int | str]]:
    return [
        {"id": department_id, "name": name}
        for department_id, name in repository.list_departments()
    ]


def update_department(
    department_id: int,
    data: DepartmentUpdate,
) -> dict[str, int | str]:
    old_name = repository.get_department(department_id)
    if old_name is None:
        raise DepartmentNotFound

    existing = repository.find_department(data.name)
    if existing and existing.lower() != old_name.lower():
        raise DepartmentAlreadyExists

    new_name = data.name.strip()
    for employee in repository.list_employees():
        if employee["department"].lower() == old_name.lower():
            repository.update_employee(employee["id"], {"department": new_name})

    repository.update_department(department_id, new_name)
    return {
        "id": department_id,
        "name": new_name,
    }


def delete_department(department_id: int) -> None:
    department_name = repository.get_department(department_id)
    if department_name is None:
        raise DepartmentNotFound

    for employee in repository.list_employees():
        if employee["department"].lower() == department_name.lower():
            raise DepartmentHasEmployees

    repository.remove_department(department_id)
