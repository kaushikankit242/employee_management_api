import json
from pathlib import Path

from APP.security import hash_password, verify_password, create_access_token

DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "users.json"


def read_users():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_users(users):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4)


def register_user(user_data):
    users = read_users()

    for user in users:
        if user["username"] == user_data.username:
            return None

        if user["email"].lower() == user_data.email.lower():
            return None

    new_user = {
        "username": user_data.username,
        "email": user_data.email,
        "hashed_password": hash_password(user_data.password),
    }

    users.append(new_user)
    save_users(users)

    return {
        "username": new_user["username"],
        "email": new_user["email"],
    }


def login_user(user_data):
    users = read_users()

    for user in users:
        if user["username"] == user_data.username:
            if verify_password(
                user_data.password,
                user["hashed_password"],
            ):
                token = create_access_token(user["username"])

                return {
                    "access_token": token,
                    "token_type": "bearer",
                }

    return None


def find_user(username):
    users = read_users()

    for user in users:
        if user["username"] == username:
            return {
                "username": user["username"],
                "email": user["email"],
            }

    return None