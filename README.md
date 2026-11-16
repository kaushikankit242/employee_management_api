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

Create a PostgreSQL database named `employee_db`, then copy the example
environment file and update the database password and JWT secret:

```powershell
Copy-Item .env.example .env
```

Set `DB_PASSWORD` to your PostgreSQL password and `SECRET_KEY` to a secure,
random value in `.env`. The application loads and validates these settings at
startup. PostgreSQL must already be running and the database must already
exist. The real `.env` file is excluded from Git; share only `.env.example`.

## Create the first user

The public registration endpoint is disabled. To create the initial account,
run this from the project root:

```powershell
poetry run python -m scripts.admin
```

The script prompts for a username, email, and password, stores a password hash,
and only runs when the `users` table is empty. This project does not currently
have user roles, so this first account is not distinct from other authenticated
users in the API.

## Run

```powershell
poetry run uvicorn main:app --reload
```

The API is available at <http://127.0.0.1:8000>. Interactive API documentation
is available at <http://127.0.0.1:8000/docs>.

## API versioning

New API requests should use the `/api/v1` prefix. For example:

- `POST /api/v1/auth/login`
- `GET /api/v1/employees/`
- `GET /api/v1/departments/`
- `GET /api/v1/users/me`

The root health check remains at `/`. Existing unversioned API paths continue
to work for compatibility, but Swagger documents the versioned paths. Future
breaking API changes can be introduced under a new prefix such as `/api/v2`.

## Project layout

- `main.py` - creates the FastAPI application and registers its routes.
- `app/middlewares/` - CORS middleware configuration.
- `app/routers/` - authentication, employee, and department endpoints.
- `app/managers/` - application logic.
- `app/database.py` and `app/model.py` - PostgreSQL connection and SQLAlchemy ORM models.
- `app/schemas/` - request and response schemas.
- `scripts/admin.py` - one-time first-user bootstrap script.
- `data/` - JSON data used for authentication.
