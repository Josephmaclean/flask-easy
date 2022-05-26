"""
response.py

Author: Joseph Maclean Arhin
"""
import typing as t
from marshmallow import Schema


class ResponseEntity:
    """Response entity to parse response from views"""

    _value = None
    _res_schema = None
    _many = False
    _status_code = None
    _mimetype = None

    def __init__(
        self,
        value: t.Any,
        status_code: int,
        schema: t.Optional[t.Type[Schema]],
        **kwargs
    ):
        self._value = value
        self._res_schema = schema
        self._many = kwargs.get("many", False)
        self._status_code = status_code
        self._mimetype = kwargs.get("mimetype", None)

    @classmethod
    def created(cls, data=None):
        """
        Created https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/201
        :param data:
        :return:
        """
        cls._status_code = 201
        cls._value = data
        return cls._response()

    @classmethod
    def bad_request(cls):
        """
        Bad Request
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/403
        :return:
        """
        cls._status_code = 403
        return cls._response()

    @classmethod
    def ok(cls, data=None):  # pylint: disable=C0103
        """
        Okay
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/200
        :param data:
        :return:
        """
        cls._status_code = 200
        cls._value = data
        return cls._response()

    @classmethod
    def body(cls, data=None):
        """
        Add body to response data
        :param data:
        :return:
        """
        cls._value = data
        return cls._response()

    @classmethod
    def schema(cls, schema: t.Optional[t.Type[Schema]], many=False):
        """
        Add marshmallow schema to serialize data
        :param many:
        :param schema:
        :return:
        """
        cls._res_schema = schema
        cls._many = many
        return cls._response()

    @classmethod
    def headers(cls, headers: dict):
        """
        set response headers
        :param headers:
        :return:
        """
        cls.headers = headers
        return cls._response()

    @classmethod
    def status(cls, status_code: int):
        """
        set response http status code
        :param status_code:
        :return:
        """
        cls._status_code = status_code
        return cls._response()

    @classmethod
    def _response(cls):
        """
        return class instance
        :return: class
        """
        return cls(
            value=cls._value,
            status_code=cls._status_code,
            schema=cls._res_schema,
            many=cls._many,
        )

    @property
    def values(self):
        """return all class values"""
        return {
            "value": self._value,
            "schema": self._res_schema,
            "many": self._many,
            "status": self._status_code,
            "mimetype": self._mimetype,
        }
