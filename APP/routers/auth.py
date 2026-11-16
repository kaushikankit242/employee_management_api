
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.managers.auth import find_user, login_user
from app.schemas.auth import TokenResponse, UserLogin, UserResponse
from app.security import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/login", response_model=TokenResponse)
def login(
    user: UserLogin,
    db: Annotated[Session, Depends(get_db)],
) -> dict[str, str]:
    result = login_user(db, user)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return result


@router.get("/me", response_model=UserResponse)
def get_my_profile(
    username: Annotated[str, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> dict[str, str]:
    user = find_user(db, username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user
