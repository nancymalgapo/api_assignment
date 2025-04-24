from enum import Enum
from fastapi import HTTPException, status


class ErrorTypes(str, Enum):
    UNKNOWN = "unknown"
    BAD_REQUEST = "bad_request"
    NOT_FOUND = "not_found"
    INTERNAL_SERVER_ERROR = "internal_server_error"


class BaseAppException(HTTPException):
    http_status_code: int
    error_type: ErrorTypes
    details: str

    def __init__(self):
        super().__init__(status_code=self.http_status_code, detail=self.details)


class BadRequest(BaseAppException):
    http_status_code = status.HTTP_400_BAD_REQUEST
    error_type = ErrorTypes.BAD_REQUEST
    details = "Bad request"


class NotFound(BaseAppException):
    http_status_code = status.HTTP_404_NOT_FOUND
    error_type = ErrorTypes.NOT_FOUND
    details = "Not Found"


class InternalServerError(BaseAppException):
    http_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_type = ErrorTypes.INTERNAL_SERVER_ERROR
    details = "Internal Server Error"
