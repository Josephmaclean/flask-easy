"""
peewee_sql_repository.py

Author: Joseph Maclean Arhin
"""
import typing as t

from peewee import PeeweeException
from flask_easy import db

from ..exc import OperationError
from .repository_interface import RepositoryInterface


IdType = t.Union[int, str]


class Repository(RepositoryInterface):
    """SqlRepository interface using Peewee"""

    model: t.Type[db.Model]

    @classmethod
    def index(cls):
        try:
            return cls.model.select()
        except PeeweeException as error:
            raise OperationError(error.args[0]) from error

    @classmethod
    def create(cls, data: dict):
        try:
            db_obj = cls.model(**data)
            db_obj.save()
            return db_obj
        except PeeweeException as error:
            raise OperationError(error.args[0]) from error

    @classmethod
    def create_all(cls, data: t.List[dict]):
        try:
            cls.model.insert_many(data).execute()
        except PeeweeException as error:
            raise OperationError(error.args[0]) from error

    @classmethod
    def find_by_id(cls, obj_id: IdType):
        try:
            return cls.model.get_by_id(obj_id)
        except PeeweeException as error:
            raise OperationError(error.args[0]) from error

    @classmethod
    def update_by_id(cls, obj_id: IdType, data: dict):
        try:
            return cls.model.update(**data).where(cls.model.id == obj_id)
        except PeeweeException as error:
            raise OperationError(error.args[0]) from error

    @classmethod
    def find(cls, query_params: dict):
        pass

    @classmethod
    def find_all(cls, query_params: dict):
        pass

    @classmethod
    def delete(cls, obj_id: IdType):
        try:
            cls.model.delete_by_id(obj_id)
            return True
        except PeeweeException as error:
            raise OperationError(error.args[0]) from error
