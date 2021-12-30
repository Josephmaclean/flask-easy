"""
This module contains ServiceResult and handle_result
"""
import typing

from marshmallow import Schema
from flask import Response, json


class ServiceResult:
    """
    Service Result
    """
    __slots__ = ["value", "status_code", "headers"]

    def __init__(self, value, status_code, headers=None):
        self.status_code = status_code
        self.value = value
        self.headers = headers


def handle_result(result: typing.Union[tuple, ServiceResult], schema: Schema=None, many=False):
    """
    convert result returned from services to http result
    :param result: result returned from service
    :param schema: marshmallow schema to serialize data
    :param many:
    :return:
    """
    if isinstance(result, tuple):
        value, status_code = result
        headers = None

    elif isinstance(result, ServiceResult):
        value = result.value
        status_code = result.status_code
        headers = result.headers

    if schema:
        return Response(
            schema(many=many).dumps(value),
            status=status_code,
            mimetype="application/json",
            headers=headers,
        )
    else:
        return Response(
            json.dumps(value),
            status=status_code,
            mimetype="application/json",
            headers=None,
        )
