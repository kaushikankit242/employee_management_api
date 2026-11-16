from data import store

from ..exceptions import DepartmentNotFound, EmployeeNotFound


def get_employee(employee_id: int) -> dict | None:
    for employee in store.load_data()["employees"]:
        if employee["id"] == employee_id:
            return employee
    return None


def list_employees() -> list[dict]:
    return store.load_data()["employees"]


def add_employee(employee: dict) -> int:
    with store.DATA_LOCK:
        data = store.load_data()
        employee_id = data["next_employee_id"]
        data["next_employee_id"] += 1
        employee["id"] = employee_id
        data["employees"].append(employee)
        store.save_data(data)
        return employee_id


def update_employee(employee_id: int, changes: dict) -> dict:
    with store.DATA_LOCK:
        data = store.load_data()
        for employee in data["employees"]:
            if employee["id"] == employee_id:
                employee.update(changes)
                store.save_data(data)
                return employee
    raise EmployeeNotFound


def remove_employee(employee_id: int) -> None:
    with store.DATA_LOCK:
        data = store.load_data()
        data["employees"] = [
            employee for employee in data["employees"]
            if employee["id"] != employee_id
        ]
        store.save_data(data)


def get_department(department_id: int) -> str | None:
    for department in store.load_data()["departments"]:
        if department["id"] == department_id:
            return department["name"]
    return None


def find_department(name: str) -> str | None:
    normalized_name = name.strip().lower()
    for department in store.load_data()["departments"]:
        department_name = department["name"]
        if department_name.lower() == normalized_name:
            return department_name
    return None


def list_departments() -> list[tuple[int, str]]:
    return [
        (department["id"], department["name"])
        for department in store.load_data()["departments"]
    ]


def add_department(name: str) -> int:
    with store.DATA_LOCK:
        data = store.load_data()
        department_id = data["next_department_id"]
        data["next_department_id"] += 1
        data["departments"].append({"id": department_id, "name": name})
        store.save_data(data)
        return department_id


def update_department(department_id: int, name: str) -> None:
    with store.DATA_LOCK:
        data = store.load_data()
        for department in data["departments"]:
            if department["id"] == department_id:
                department["name"] = name
                store.save_data(data)
                return
    raise DepartmentNotFound


def remove_department(department_id: int) -> None:
    with store.DATA_LOCK:
        data = store.load_data()
        data["departments"] = [
            department for department in data["departments"]
            if department["id"] != department_id
        ]
        store.save_data(data)
