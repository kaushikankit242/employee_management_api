import os
from pathlib import Path

from dotenv import load_dotenv

ENV_FILE = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(ENV_FILE)

REQUIRED_ENV_VARS = (
    "APP_NAME",
    "APP_VERSION",
    "DEBUG",
    "DB_HOST",
    "DB_PORT",
    "DB_NAME",
    "DB_USER",
    "DB_PASSWORD",
    "SECRET_KEY",
    "ALGORITHM",
    "ACCESS_TOKEN_EXPIRE_MINUTES",
    "FRONTEND_URL",
)

missing_vars = [
    name for name in REQUIRED_ENV_VARS
    if not os.getenv(name, "").strip()
]
if missing_vars:
    missing_list = ", ".join(missing_vars)
    raise RuntimeError(
        f"Missing required environment variables: {missing_list}. "
        f"Set them in {ENV_FILE} or the process environment."
    )


def _read_int(name: str) -> int:
    value = os.environ[name]
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer.") from exc


def _read_bool(name: str) -> bool:
    value = os.environ[name].strip().lower()
    if value in {"true", "1", "yes", "on"}:
        return True
    if value in {"false", "0", "no", "off"}:
        return False
    raise ValueError(f"{name} must be a boolean (true or false).")


APP_NAME = os.environ["APP_NAME"].strip()
APP_VERSION = os.environ["APP_VERSION"].strip()
DEBUG = _read_bool("DEBUG")

DB_HOST = os.environ["DB_HOST"].strip()
DB_PORT = _read_int("DB_PORT")
DB_NAME = os.environ["DB_NAME"].strip()
DB_USER = os.environ["DB_USER"].strip()
DB_PASSWORD = os.environ["DB_PASSWORD"]

if not 1 <= DB_PORT <= 65535:
    raise ValueError("DB_PORT must be between 1 and 65535.")

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"].strip()
ACCESS_TOKEN_EXPIRE_MINUTES = _read_int("ACCESS_TOKEN_EXPIRE_MINUTES")
if ACCESS_TOKEN_EXPIRE_MINUTES <= 0:
    raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES must be positive.")

FRONTEND_URL = os.environ["FRONTEND_URL"].strip()
