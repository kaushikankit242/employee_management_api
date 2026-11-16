from typing import Literal

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.cores.loggers import logger

from ..exceptions import (
    DepartmentDoesNotExist,
    EmailAlreadyExists,
    EmployeeNotFound,
    NullUpdateField,
)
from ..model import Department, Employee
from ..schemas.models import EmployeeCreate, EmployeeUpdate, StatusUpdate


def _employee_response(employee: Employee) -> dict:
    return {
        "id": employee.id,
        "name": employee.name,
        "email": employee.email,
        "department": employee.department.name,
        "designation": employee.designation,
        "salary": employee.salary,
        "status": employee.status,
    }


def _find_department(db: Session, name: str) -> Department | None:
    return db.scalar(
        select(Department).where(func.lower(Department.name) == name.strip().lower())
    )


def _email_exists(db: Session, email: str, exclude_id: int | None = None) -> bool:
    query = select(Employee.id).where(func.lower(Employee.email) == email.lower())
    if exclude_id is not None:
        query = query.where(Employee.id != exclude_id)
    return db.scalar(query) is not None


def create_employee(db: Session, data: EmployeeCreate) -> dict:
    logger.info("Employee data processing started")
    department = _find_department(db, data.department)
    if department is None:
        raise DepartmentDoesNotExist

    if _email_exists(db, data.email):
        raise EmailAlreadyExists

    employee = Employee(
        name=data.name,
        email=data.email,
        department=department,
        designation=data.designation,
        salary=data.salary,
        status=data.status,
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return _employee_response(employee)


def get_all_employees(
    db: Session,
    department: str | None = None,
    employee_status: Literal["Active", "Inactive"] | None = None,
    search: str | None = None,
) -> dict:
    query = select(Employee).join(Employee.department)
    if department:
        query = query.where(func.lower(Department.name) == department.lower())
    if employee_status:
        query = query.where(Employee.status == employee_status)
    if search:
        term = f"%{search.strip()}%"
        query = query.where(
            or_(
                Employee.name.ilike(term),
                Employee.email.ilike(term),
                Employee.designation.ilike(term),
            )
        )

    employees = [_employee_response(employee) for employee in db.scalars(query).all()]
    return {"total": len(employees), "employees": employees}


def get_one_employee(db: Session, employee_id: int) -> dict:
    employee = db.get(Employee, employee_id)
    if employee is None:
        logger.warning("Requested employee was not found")
        raise EmployeeNotFound
    return _employee_response(employee)


def replace_employee(db: Session, employee_id: int, data: EmployeeCreate) -> dict:
    employee = db.get(Employee, employee_id)
    if employee is None:
        logger.warning("Requested employee was not found")
        raise EmployeeNotFound

    department = _find_department(db, data.department)
    if department is None:
        raise DepartmentDoesNotExist
    if _email_exists(db, data.email, exclude_id=employee_id):
        raise EmailAlreadyExists

    employee.name = data.name
    employee.email = data.email
    employee.department = department
    employee.designation = data.designation
    employee.salary = data.salary
    employee.status = data.status
    db.commit()
    db.refresh(employee)
    return _employee_response(employee)


def update_employee(db: Session, employee_id: int, data: EmployeeUpdate) -> dict:
    employee = db.get(Employee, employee_id)
    if employee is None:
        logger.warning("Requested employee was not found")
        raise EmployeeNotFound

    changes = data.model_dump(exclude_unset=True)
    for field, value in changes.items():
        if value is None:
            raise NullUpdateField(field)

    if "department" in changes:
        department = _find_department(db, changes.pop("department"))
        if department is None:
            raise DepartmentDoesNotExist
        employee.department = department
    if "email" in changes and _email_exists(
        db, changes["email"], exclude_id=employee_id
    ):
        raise EmailAlreadyExists

    for field, value in changes.items():
        setattr(employee, field, value)
    db.commit()
    db.refresh(employee)
    return _employee_response(employee)


def update_employee_status(
    db: Session,
    employee_id: int,
    data: StatusUpdate,
) -> dict:
    employee = db.get(Employee, employee_id)
    if employee is None:
        logger.warning("Requested employee was not found")
        raise EmployeeNotFound
    employee.status = data.status
    db.commit()
    db.refresh(employee)
    return _employee_response(employee)


def delete_employee(db: Session, employee_id: int) -> None:
    employee = db.get(Employee, employee_id)
    if employee is None:
        logger.warning("Requested employee was not found")
        raise EmployeeNotFound
    db.delete(employee)
    db.commit()
