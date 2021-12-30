"""
App Exceptions
"""

from typing import Optional
from flask import current_app as app


class AppExceptionCase(Exception):
    """
    Base exception case to be inherited by all other exceptions
    """

    def __init__(self, status_code: int, message):
        """

        :param status_code:
        :param message: extra data to give the error more context
        """
        app.logger.error(message)
        self.exception_case = self.__class__.__name__
        self.status_code = status_code
        self.context = message

    def __str__(self):
        return (
            f"<AppException {self.exception_case} - "
            + f"status_code = {self.status_code} - message = {self.context}"
        )


class InternalServerError(AppExceptionCase):
    """
    Generic Exception to catch failed operations
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/500
    """

    def __init__(self, message):
        status_code = 500
        AppExceptionCase.__init__(self, status_code, message)


class OperationError(InternalServerError):
    """
    Generic Exception to catch failed operations
    """


class NotFoundException(AppExceptionCase):
    """
    Not found exception
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404
    """

    def __init__(self, message="Resource not found"):
        status_code = 404
        AppExceptionCase.__init__(self, status_code, message)


class Unauthorized(AppExceptionCase):
    """
    Unauthorized
    """
    def __init__(self, message="Unauthorized", status_code=401):
        """
        Unauthorized
        :param message: extra dictionary object to give the error more context
        """
        AppExceptionCase.__init__(self, status_code, message)


class BadRequest(AppExceptionCase):
    """
    Raised when there's a bad request
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400
    """

    def __init__(self, message=None):
        """
        Bad Request

        :param message:
        """
        status_code = 400
        AppExceptionCase.__init__(self, status_code, message)


class ResourceExists(BadRequest):
    """
    Resource Exists
    """


class ValidationException(BadRequest):
    """
    Validation Exception
    """


class ExpiredTokenException(BadRequest):
    """
    Raised when a token is expired
    """


class SetupError(Exception):
    description: Optional[str] = None

    def __init__(self, description: Optional[str] = None):
        if description:
            self.description = description


class DBConnectionException(SetupError):
    pass
