"""
mongo_repository.py

Author: Joseph Maclean Arhin
"""

import typing as t

import mongoengine as me

from ..exc import OperationError, NotFoundException
from .repository_interface import RepositoryInterface


class Repository(RepositoryInterface):
    """
    Repository to be inherited
    """

    model: t.Type[me.Document]

    @classmethod
    def index(cls) -> t.List[me.Document]:
        """
        gets all documents in a mongodb collection
        :return: list of mongodb documents
        """
        try:
            return cls.model.objects()
        except me.OperationError as error:
            raise OperationError([error.args[0]]) from error

    @classmethod
    def create(cls, data: dict) -> t.Type[me.Document]:
        """
        creates a mongodb document with the data passed to it
        :param data: data to persist in the database
        :return: mongodb document
        """
        try:
            db_obj = cls.model(**data)
            db_obj.save()
            return db_obj
        except me.OperationError as error:
            raise OperationError([error.args[0]]) from error

    @classmethod
    def create_all(cls, data: t.List[dict]) -> t.List[t.Type[me.Document]]:
        try:
            obj_data = [cls.model(**item) for item in data]
            return cls.model.objects.insert(obj_data)
        except me.OperationError as error:
            raise OperationError([error.args[0]]) from error

    @classmethod
    def update_by_id(cls, obj_id: t.Union[int, str], data: dict) -> t.Type[me.Document]:
        """

        :param obj_id:
        :param data:
        :return:
        """
        try:
            db_obj = cls.find_by_id(obj_id)
            db_obj.modify(**data)
            return db_obj
        except me.OperationError as error:
            raise OperationError([error.args[0]]) from error

    @classmethod
    def find(cls, query_params: dict) -> t.Type[me.Document]:
        """
        returns an item that satisfies the data passed to it if it exists in
        the database

        :param query_params: {dict}
        :return: model_object - Returns an instance object of the model passed
        """
        try:
            db_obj = cls.model.objects.get(**query_params)
            return db_obj
        except me.DoesNotExist as error:
            raise NotFoundException({"error": "Resource does not exist"}) from error
        except me.OperationError as error:
            raise OperationError([error.args[0]]) from error

    @classmethod
    def find_all(cls, query_params: dict) -> t.List[t.Type[me.Document]]:
        """
        returns all items that satisfy the filter query_params passed to it

        :param query_params: query parameters to filter by
        :return: model_object - Returns an instance object of the model passed
        """
        try:
            db_obj = cls.model.objects(**query_params)
            return db_obj

        except me.OperationError as error:
            raise OperationError([error.args[0]]) from error

    @classmethod
    def find_by_id(cls, obj_id: t.Union[int, str]) -> t.Type[me.Document]:
        try:
            db_obj = cls.model.objects.get(pk=obj_id)
            return db_obj
        except me.DoesNotExist as error:
            raise NotFoundException(
                {"error": f"Resource of id {obj_id} does not exist"}
            ) from error
        except me.OperationError as error:
            raise OperationError([error.args[0]]) from error

    @classmethod
    def delete(cls, obj_id: t.Union[int, str]) -> bool:
        """
        delete an object matching the id
        :param obj_id: id of object to be deleted
        :return:
        """
        try:
            db_obj = cls.model.objects.get(pk=obj_id)
            db_obj.delete()
            return True
        except me.DoesNotExist as error:
            raise NotFoundException(
                {"error": f"Resource of id {obj_id} does not exist"}
            ) from error
        except me.OperationError as error:
            raise OperationError([error.args[0]]) from error
