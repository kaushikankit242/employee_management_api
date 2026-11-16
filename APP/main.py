from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI

from app.config import APP_NAME, APP_VERSION, DEBUG
from app.cores.loggers import logger
from app.database import create_db_and_tables
from app.middlewares.cors import add_cors_middleware
from app.routers import auth, departments, employees
from app.security import get_current_user

api_v1_router = APIRouter()
api_v1_router.include_router(auth.router, prefix="/api/v3")
api_v1_router.include_router(employees.router, prefix="/api/v1")
api_v1_router.include_router(departments.router, prefix="/api/v2")


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
    logger.info("Employee Management API starting")
    create_db_and_tables()
    yield
    logger.info("Employee Management API shutting down")


app = FastAPI(
    title=APP_NAME,
    description="Employee Management with JWT Authentication",
    version=APP_VERSION,
    debug=DEBUG,
    lifespan=lifespan,
)
add_cors_middleware(app)





@api_v1_router.get("/users/me")
def get_user(current_user: Annotated[str, Depends(get_current_user)]):
    return {
        "message": "Access granted",
        "user": current_user
    }


app.include_router(api_v1_router)


app.include_router(auth.router, include_in_schema=False)
app.include_router(employees.router, include_in_schema=False)
app.include_router(departments.router, include_in_schema=False)
app.add_api_route(
    "/users/me",
    get_user,
    methods=["GET"],
    include_in_schema=False,
)