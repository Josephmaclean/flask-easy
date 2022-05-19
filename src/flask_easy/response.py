import dataclasses
import typing as t
from marshmallow import Schema


class ResponseEntity(object):
    value = None
    res_schema = None
    many = False
    status_code = None
    def __init__(
            self,
            value: t.Any,
            status_code: int,
            schema: t.Optional[t.Type[Schema]],
            many: bool = False,

    ):
        self.value = value
        self.res_schema = schema
        self.many = many
        self.status_code = status_code

    @classmethod
    def created(cls, data=None):
        cls.status_code = 201
        cls.value = data
        return cls.response()

    @classmethod
    def bad_request(cls):
        cls.status_code = 403
        return cls.response()

    @classmethod
    def ok(cls, data=None):
        cls.status_code=200
        cls.value = data
        return cls.response()

    @classmethod
    def body(cls, data=None):
        cls.value = data
        return cls.response()

    @classmethod
    def schema(cls, schema:t.Optional[t.Type[Schema]]):
        cls.res_schema = schema
        return cls.response()

    @classmethod
    def set_headers(cls, headers:dict):
        cls.headers = headers
        return cls.response()

    @classmethod
    def response(cls):
        return cls(value=cls.value, status_code=cls.status_code, schema=cls.res_schema, many=cls.many)
