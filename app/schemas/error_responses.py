from typing import Any, Dict, Union

from pydantic import BaseModel


class Error(BaseModel):
    message: str


HEALTH_ERROR_RESPONSES: Dict[Union[int, str], Dict[str, Any]] = {
    500: {"model": Error, "description": "Server error"}
}

ERROR_RESPONSES: Dict[Union[int, str], Dict[str, Any]] = HEALTH_ERROR_RESPONSES | {
    400: {"model": Error, "description": "Invalid request"},
    401: {
        "model": Error,
        "description": "Unauthorized request",
    },
    403: {"model": Error, "description": "Forbidden"},
}

SINGLE_RESOURCE_ERROR_RESPONSES: Dict[
    Union[int, str], Dict[str, Any]
] = ERROR_RESPONSES | {
    404: {"model": Error, "description": "Not found"},
}
