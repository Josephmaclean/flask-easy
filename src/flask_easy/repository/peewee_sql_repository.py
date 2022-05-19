from typing import Union, Optional, Type, List

from peewee import PeeweeException
from flask_easy import db

from ..exc import NotFoundException, OperationError
from .repository_interface import RepositoryInterface


IdType = Union[int, str]


class PeeweeSqlRepository(RepositoryInterface):
    model: Type[db.Model]

    @classmethod
    def index(cls):
        try:
            return cls.model.select()
        except PeeweeException as e:
            raise OperationError(e.args[0])

    @classmethod
    def create(cls, data: dict):
        try:
            db_obj = cls.model(**data)
            db_obj.save()
            return db_obj
        except PeeweeException as e:
            raise OperationError(e.args[0])

    @classmethod
    def create_all(self, data: List[dict]):
        try:
            self.model.insert_many(data).execute()
        except PeeweeException as e:
            raise OperationError(e.args[0])

    @classmethod
    def find_by_id(self, obj_id: IdType):
        try:
            return self.model.get_by_id(obj_id)
        except PeeweeException as e:
            raise OperationError(e.args[0])
