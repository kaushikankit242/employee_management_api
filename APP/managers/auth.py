from sqlalchemy import func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.model import AuthUser
from app.schemas.auth import UserLogin, UserRegister
from app.security import create_access_token, hash_password, verify_password


def register_user(db: Session, user: UserRegister) -> dict[str, str] | None:
    email = str(user.email).lower()
    existing_user = db.scalar(
        select(AuthUser.id).where(
            or_(
                func.lower(AuthUser.username) == user.username.lower(),
                func.lower(AuthUser.email) == email,
            )
        )
    )
    if existing_user is not None:
        return None

    new_user = AuthUser(
        username=user.username,
        email=email,
        hashed_password=hash_password(user.password),
    )
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return None

    return {"username": new_user.username, "email": new_user.email}


def login_user(db: Session, user: UserLogin) -> dict[str, str] | None:
    existing_user = db.scalar(
        select(AuthUser).where(func.lower(AuthUser.username) == user.username.lower())
    )
    if existing_user is None or not verify_password(
        user.password,
        existing_user.hashed_password,
    ):
        return None

    return {
        "access_token": create_access_token(existing_user.username),
        "token_type": "bearer",
    }


def find_user(db: Session, username: str) -> dict[str, str] | None:
    user = db.scalar(
        select(AuthUser).where(func.lower(AuthUser.username) == username.lower())
    )
    if user is None:
        return None

    return {"username": user.username, "email": user.email}
