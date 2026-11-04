from fastapi import APIRouter, Depends, HTTPException, status

from APP.schema.auth import (
    UserLogin,
    UserResponse,
    TokenResponse,
)

from APP.manager.auth import (
    login_user,
    find_user,
)

from APP.security import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin):
    result = login_user(user)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return result


@router.get("/me", response_model=UserResponse)
def get_my_profile(username: str = Depends(get_current_user)):
    user = find_user(username)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )

    return user