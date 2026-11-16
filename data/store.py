import json
import os
import tempfile
from pathlib import Path
from threading import RLock
from typing import TypedDict

from app.exceptions import InvalidStoreData


class EmployeeRecord(TypedDict):
    id: int
    name: str
    email: str
    department: str
    designation: str
    salary: float
    status: str


class DepartmentRecord(TypedDict):
    id: int
    name: str


class StoreData(TypedDict):
    employees: list[EmployeeRecord]
    departments: list[DepartmentRecord]
    next_employee_id: int
    next_department_id: int


DATA_FILE = Path(__file__).with_name("data.json")
DATA_LOCK = RLock()
INITIAL_DATA: StoreData = {
    "employees": [],
    "departments": [
        {"id": 1, "name": "IT"},
        {"id": 2, "name": "HR"},
        {"id": 3, "name": "Sales"},
    ],
    "next_employee_id": 1,
    "next_department_id": 4,
}


def load_data() -> StoreData:
    with DATA_LOCK:
        if not DATA_FILE.exists():
            save_data(INITIAL_DATA)

        with DATA_FILE.open(encoding="utf-8") as data_file:
            data = json.load(data_file)

        expected_keys = {
            "employees",
            "departments",
            "next_employee_id",
            "next_department_id",
        }
        if not isinstance(data, dict) or set(data) != expected_keys:
            raise InvalidStoreData(f"Invalid JSON data structure in {DATA_FILE}")
        if not isinstance(data["employees"], list) or not isinstance(
            data["departments"], list
        ):
            raise InvalidStoreData(f"Invalid record collections in {DATA_FILE}")
        if not isinstance(data["next_employee_id"], int) or not isinstance(
            data["next_department_id"], int
        ):
            raise InvalidStoreData(f"Invalid ID counters in {DATA_FILE}")

        return data


def save_data(data: StoreData) -> None:
    with DATA_LOCK:
        temporary_path: str | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=DATA_FILE.parent,
                suffix=".tmp",
                delete=False,
            ) as temporary_file:
                temporary_path = temporary_file.name
                json.dump(data, temporary_file, indent=2)
                temporary_file.write("\n")

            os.replace(temporary_path, DATA_FILE)
        finally:
            if temporary_path is not None and os.path.exists(temporary_path):
                os.unlink(temporary_path)
