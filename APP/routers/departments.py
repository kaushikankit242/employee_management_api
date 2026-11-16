from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.security import get_current_user

from ..database import get_db
from ..managers import departments as department_manager
from ..schemas.models import DepartmentCreate, DepartmentUpdate
from .responses import success_response

router = APIRouter(
    prefix="/departments",
    tags=["departments"],
    dependencies=[Depends(get_current_user)],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_department_route(
    data: DepartmentCreate,
    response: Response,
    db: Annotated[Session, Depends(get_db)],
) -> dict:
    department = department_manager.create_department(db, data)
    return success_response(
        response,
        "Department created successfully",
        department,
        status.HTTP_201_CREATED,
    )


@router.get("/")
def get_departments_route(
    response: Response,
    db: Annotated[Session, Depends(get_db)],
) -> dict:
    departments = department_manager.get_departments(db)
    return success_response(
        response,
        "Departments retrieved successfully",
        departments,
    )


@router.patch("/{department_id}")
def update_department_route(
    department_id: int,
    data: DepartmentUpdate,
    response: Response,
    db: Annotated[Session, Depends(get_db)],
) -> dict:
    department = department_manager.update_department(db, department_id, data)
    return success_response(response, "Department updated successfully", department)


@router.delete("/{department_id}")
def delete_department_route(
    department_id: int,
    response: Response,
    db: Annotated[Session, Depends(get_db)],
) -> dict:
    department_manager.delete_department(db, department_id)
    return success_response(
        response,
        "Department deleted successfully",
        {"id": department_id},
    )
