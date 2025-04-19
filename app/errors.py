from enum import Enum
from fastapi import HTTPException, status


class ErrorTypes(str, Enum):
    UNKNOWN = "unknown"
    BAD_REQUEST = "bad_request"
    NOT_FOUND = "not found"
    INTERNAL_SERVER_ERROR = "internal server error"


class BaseAppException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=self.get_status_code(), detail=detail)

    def get_status_code(self):
        return status.HTTP_500_INTERNAL_SERVER_ERROR  #default

class BadRequestException(BaseAppException):
    def __init__(self, detail: str = "Bad request"):
        super().__init__(detail)

    def get_status_code(self):
        return status.HTTP_400_BAD_REQUEST

class NotFoundException(BaseAppException):
    def __init__(self, detail: str = "Not Found"):
        super().__init__(detail)

    def get_status_code(self):
        return status.HTTP_404_NOT_FOUND

class InternalServerErrorException(BaseAppException):
    def __init__(self, detail: str = "Internal Server Error"):
        super().__init__(detail)

    def get_status_code(self):
        return status.HTTP_500_INTERNAL_SERVER_ERROR
