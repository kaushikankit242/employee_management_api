from typing import Any

from fastapi import Response


def success_response(
    response: Response,
    message: str,
    data: Any,
    status_code: int = 200,
) -> dict[str, Any]:
    response.status_code = status_code
    return {
        "message": message,
        "status_code": status_code,
        "data": data,
    }
