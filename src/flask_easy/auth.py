"""
auth.py

Author: Joseph Maclean Arhin
"""
import os
import inspect
from functools import wraps

import jwt
from flask import request
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError, PyJWTError
from .exc import Unauthorized, ExpiredTokenException, OperationError


def auth_required(other_roles=None):
    """auth required decorator"""

    def authorize_user(func):
        """
        A wrapper to authorize an action using
        :param func: {function}` the function to wrap around
        :return:
        """

        @wraps(func)
        def view_wrapper(*args, **kwargs):
            authorization_header = request.headers.get("Authorization")
            if not authorization_header:
                raise Unauthorized("Missing authentication token")

            token = authorization_header.split()[1]
            try:
                key = os.getenv("JWT_SECRET")  # noqa E501
                payload = jwt.decode(
                    token, key=key, algorithms=["HS256", "RS256"]
                )  # noqa E501
                # Get realm roles from payload
                available_roles = payload.get("realm_access").get("roles")

                # Append service name to function name to form role

                # generated_role = service_name + "_" + func.__name__

                generated_role = "s"
                authorized_roles = []

                if other_roles:
                    authorized_roles = other_roles.split("|")

                authorized_roles.append(generated_role)

                if is_authorized(authorized_roles, available_roles):
                    if "user_id" in inspect.getfullargspec(func).args:
                        kwargs["user_id"] = payload.get(
                            "preferred_username"
                        )  # noqa E501
                    return func(*args, **kwargs)
            except ExpiredSignatureError as error:
                raise ExpiredTokenException("Token Expired") from error
            except InvalidTokenError as error:
                raise OperationError("Invalid Token") from error
            except PyJWTError as error:
                raise OperationError("Error decoding token") from error
            raise Unauthorized(status_code=403)

        return view_wrapper

    return authorize_user


def is_authorized(access_roles, available_roles):
    """Check if access roles is in available roles"""
    for role in access_roles:
        if role in available_roles:
            return True

    return False
