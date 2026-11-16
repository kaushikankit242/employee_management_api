from getpass import getpass

from pydantic import ValidationError
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.database import SessionLocal, create_db_and_tables
from app.model import AuthUser
from app.schemas.auth import UserRegister
from app.security import hash_password


def main() -> None:
    username = input("Username: ").strip()
    email = input("Email: ").strip()
    password = getpass("Password: ")
    if password != getpass("Confirm password: "):
        raise SystemExit("Passwords do not match.")

    try:
        user_data = UserRegister(username=username, email=email, password=password)
    except ValidationError as error:
        details = "; ".join(
            f"{'.'.join(str(part) for part in item['loc'])}: {item['msg']}"
            for item in error.errors(include_input=False)
        )
        raise SystemExit(f"Invalid user details: {details}") from None

    create_db_and_tables()
    with SessionLocal.begin() as db:
        db.execute(text("LOCK TABLE users IN EXCLUSIVE MODE"))
        if db.scalar(select(AuthUser.id).limit(1)) is not None:
            raise SystemExit(
                "The users table is not empty; the first user has already been created."
            )

        db.add(
            AuthUser(
                username=user_data.username,
                email=str(user_data.email).lower(),
                hashed_password=hash_password(user_data.password),
            )
        )
        try:
            db.flush()
        except IntegrityError as error:
            raise SystemExit(
                "Could not create the first user due to a database conflict."
            ) from error

    print(f"Created the first user: {user_data.username}")


if __name__ == "__main__":
    main()