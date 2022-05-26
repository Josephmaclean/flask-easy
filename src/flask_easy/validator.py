"""
validator.py

Author: Joseph Maclean Arhin
"""

import typing as t
from functools import wraps
from flask import request
from marshmallow import Schema

from flask_easy.exc.app_exceptions import ValidationException


def validator(schema: t.Type[Schema]):
    """
    A wrapper to validate input data using marshmallow schema
    e.g:
        @api.route("users", methods=[POST])
        @validator(schema=UserSchema)
        def create_user():
            pass

    :param schema: Marshmallow schema to validate by
    :return:
    """

    def validate_data(func):
        @wraps(func)
        def view_wrapper(*args, **kwargs):
            errors = schema().validate(request.json)
            if errors:
                raise ValidationException(message=errors)

            return func(*args, **kwargs)

        return view_wrapper

    return validate_data
