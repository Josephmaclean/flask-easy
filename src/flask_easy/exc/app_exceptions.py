from flask import current_app as app
from werkzeug.exceptions import HTTPException as WerkzeugHttpException


class HTTPException(WerkzeugHttpException):
    def __init__(self, status_code, description=None):
        self.code = status_code
        super().__init__(description=description)


class AppExceptionCase(Exception):
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


class OperationError(AppExceptionCase):
    """
    Generic Exception to catch failed operations
    """

    def __init__(self, message):
        status_code = 500
        AppExceptionCase.__init__(self, status_code, message)


class InternalServerError(AppExceptionCase):
    """
    Generic Exception to catch failed operations
    """

    def __init__(self, message):
        status_code = 500
        AppExceptionCase.__init__(self, status_code, message)


class ResourceExists(AppExceptionCase):
    """
    Resource Creation Failed Exception
    """

    def __init__(self, message):
        status_code = 400
        AppExceptionCase.__init__(self, status_code, message)


class NotFoundException(AppExceptionCase):
    def __init__(self, message="Resource not found"):
        """
        Resource does not exist
        """
        status_code = 404
        AppExceptionCase.__init__(self, status_code, message)


class Unauthorized(AppExceptionCase):
    def __init__(self, message="Unauthorized", status_code=401):
        """
        Unauthorized
        :param message: extra dictionary object to give the error more context
        """
        AppExceptionCase.__init__(self, status_code, message)


class ValidationException(AppExceptionCase):
    """
    Resource Creation Failed Exception
    """

    def __init__(self, message):
        status_code = 400
        AppExceptionCase.__init__(self, status_code, message)


class KeyCloakAdminException(AppExceptionCase):
    def __init__(self, message=None, status_code=400):
        """
        Key Cloak Error. Error with regards to Keycloak authentication
        :param message: extra data to give the error more context
        """

        AppExceptionCase.__init__(self, status_code, message)


class BadRequest(AppExceptionCase):
    def __init__(self, message=None):
        """
        Bad Request

        :param message:
        """
        status_code = 400
        AppExceptionCase.__init__(self, status_code, message)


class ExpiredTokenException(AppExceptionCase):
    def __init__(self, message=None):
        """
        Expired Token
        :param message:
        """

        status_code = 400
        AppExceptionCase.__init__(self, status_code, message)
