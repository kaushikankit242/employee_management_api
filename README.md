# Employee Management API

A FastAPI employee management API with JWT authentication and employee and
department routes.

## Requirements

- Python 3.14 or newer
- Poetry

## Setup

```powershell
poetry install
```

## Run

```powershell
poetry run uvicorn main:app --reload
```

The API is available at <http://127.0.0.1:8000>. Interactive API documentation
is available at <http://127.0.0.1:8000/docs>.

## Project layout

- `main.py` - creates the FastAPI application and registers its routes.
- `APP/routers/` - authentication, employee, and department endpoints.
- `APP/manager/` - application logic.
- `APP/storage/` and `data/` - data access and JSON data.
