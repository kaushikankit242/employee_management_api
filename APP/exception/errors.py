from fastapi import HTTPException


class EmployeeNotFound(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=404, detail="Employee not found")


class DepartmentNotFound(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=404, detail="Department not found")


class DepartmentDoesNotExist(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=400, detail="Department does not exist")


class EmailAlreadyExists(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=409, detail="Email already exists")


class DepartmentAlreadyExists(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=409, detail="Department already exists")


class NullUpdateField(HTTPException):
    def __init__(self, field: str) -> None:
        super().__init__(status_code=422, detail=f"{field} cannot be null")


class DepartmentHasEmployees(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=409,
            detail="Cannot delete a department with employees",
        )


class InvalidStoreData(RuntimeError):
    pass
