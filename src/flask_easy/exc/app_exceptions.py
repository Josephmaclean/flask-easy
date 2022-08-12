"""
App Exceptions
"""

from typing import Optional


class AppExceptionCase(Exception):
    """
    Base exception case to be inherited by all other exceptions
    """

    def __init__(self, message, **kwargs):  # pylint: disable=w0231
        """

        :param status_code:
        :param message: extra data to give the error more context
        """
        self.exception_case = self.__class__.__name__
        status = kwargs.get("status_code")
        if status:
            self.status_code = status
        self.context = (
            message if isinstance(message, dict) else {self.__class__.__name__: message}
        )

    def __str__(self):
        return (
            f"<AppException {self.exception_case} - "
            + f"_status_code = {self.status_code} - message = {self.context}"
        )


class InternalServerError(AppExceptionCase):
    """
    Generic Exception to catch failed operations
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/500
    """

    status_code = 500


class OperationError(InternalServerError):
    """
    Generic Exception to catch failed operations
    """


class NotFoundException(AppExceptionCase):
    """
    Not found exception
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404
    """

    status_code = 404


class Unauthorized(AppExceptionCase):
    """
    Unauthorized
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/401
    """

    status_code = 401


class BadRequest(AppExceptionCase):
    """
    Raised when there's a bad request
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400
    """

    status_code = 400


class ResourceExists(BadRequest):
    """
    Resource Exists
    """


class ValidationException(BadRequest):
    """
    Validation Exception
    """


class SetupError(Exception):
    """
    Setup Error
    """

    description: Optional[str] = None

    def __init__(self, description: Optional[str] = None):  # pylint: disable=w0231
        """initialize setup error"""
        if description:
            self.description = description


class DBConnectionException(SetupError):
    """Thrown when there's an error in a db connection"""
