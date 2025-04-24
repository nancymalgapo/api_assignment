from enum import Enum
from fastapi import HTTPException, status


class ErrorTypes(str, Enum):
    UNKNOWN = "unknown"
    BAD_REQUEST = "bad_request"
    NOT_FOUND = "not found"
    INTERNAL_SERVER_ERROR = "internal server error"


class ApiException(HTTPException):
    http_status_code: int
    error_type: ErrorTypes

    def __init__(self, detail: str):
        super().__init__(status_code=self.http_status_code, detail=detail)


class BadRequestException(ApiException):
    http_status_code = status.HTTP_400_BAD_REQUEST
    error_type = ErrorTypes.BAD_REQUEST


class NotFoundException(ApiException):
    http_status_code = status.HTTP_404_NOT_FOUND
    error_type = ErrorTypes.NOT_FOUND


class InternalServerErrorException(ApiException):
    http_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_type = ErrorTypes.INTERNAL_SERVER_ERROR
