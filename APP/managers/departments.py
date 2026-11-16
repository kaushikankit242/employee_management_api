from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..exceptions import (
    DepartmentAlreadyExists,
    DepartmentHasEmployees,
    DepartmentNotFound,
)
from ..model import Department, Employee
from ..schemas.models import DepartmentCreate, DepartmentUpdate


def create_department(db: Session, data: DepartmentCreate) -> dict[str, int | str]:
    department_name = data.name.strip()
    existing = db.scalar(
        select(Department.id).where(
            func.lower(Department.name) == department_name.lower()
        )
    )
    if existing is not None:
        raise DepartmentAlreadyExists

    department = Department(name=department_name)
    db.add(department)
    db.commit()
    db.refresh(department)
    return {"id": department.id, "name": department.name}


def get_departments(db: Session) -> list[dict[str, int | str]]:
    departments = db.scalars(select(Department).order_by(Department.id)).all()
    return [{"id": department.id, "name": department.name} for department in departments]


def update_department(
    db: Session,
    department_id: int,
    data: DepartmentUpdate,
) -> dict[str, int | str]:
    department = db.get(Department, department_id)
    if department is None:
        raise DepartmentNotFound

    new_name = data.name.strip()
    existing = db.scalar(
        select(Department.id).where(
            func.lower(Department.name) == new_name.lower(),
            Department.id != department_id,
        )
    )
    if existing is not None:
        raise DepartmentAlreadyExists

    department.name = new_name
    db.commit()
    db.refresh(department)
    return {"id": department.id, "name": department.name}


def delete_department(db: Session, department_id: int) -> None:
    department = db.get(Department, department_id)
    if department is None:
        raise DepartmentNotFound
    has_employees = db.scalar(
        select(Employee.id).where(Employee.department_id == department_id).limit(1)
    )
    if has_employees is not None:
        raise DepartmentHasEmployees

    db.delete(department)
    db.commit()
