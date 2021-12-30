from typing import Type, List, Union

import mongoengine as me

from ..exc import OperationError, NotFoundException
from .repository_interface import RepositoryInterface


class MongoRepository(RepositoryInterface):
    model: Type[me.Document]

    def index(self) -> List[me.Document]:
        """
        gets all documents in a mongodb collection
        :return: list of mongodb documents
        """
        try:
            return self.model.objects()
        except me.OperationError as error:
            raise OperationError([error.args[0]])

    def create(self, data: dict):
        """
        creates a mongodb document with the data passed to it
        :param data: data to persist in the database
        :return: mongodb document
        """
        try:
            db_obj = self.model(**data)
            db_obj.save()
            return db_obj
        except me.OperationError as error:
            raise OperationError([error.args[0]])

    def create_all(self, data: List[dict]):
        try:
            obj_data = [self.model(**item) for item in data]
            return self.model.objects.insert(obj_data)
        except me.OperationError as error:
            raise OperationError([error.args[0]])

    def update_by_id(self, obj_id: Union[int, str], data: dict):
        """

        :param obj_id:
        :param data:
        :return:
        """
        try:
            db_obj = self.find_by_id(obj_id)
            db_obj.modify(**data)
            return db_obj
        except me.OperationError as error:
            raise OperationError([error.args[0]])

    def find(self, query_params: dict):
        """
        returns an item that satisfies the data passed to it if it exists in
        the database

        :param query_params: {dict}
        :return: model_object - Returns an instance object of the model passed
        """
        try:
            db_obj = self.model.objects.get(**query_params)
            return db_obj
        except me.DoesNotExist:
            raise NotFoundException({"error": "Resource does not exist"})
        except me.OperationError as error:
            raise OperationError([error.args[0]])

    def find_all(self, query_params: dict):
        """
        returns all items that satisfies the filter query_params passed to it

        :param query_params: query parameters to filter by
        :return: model_object - Returns an instance object of the model passed
        """
        try:
            db_obj = self.model.objects(**query_params)
            return db_obj

        except me.OperationError as error:
            raise OperationError([error.args[0]])

    def find_by_id(self, obj_id: Union[int, str]):
        try:
            db_obj = self.model.objects.get(pk=obj_id)
            return db_obj
        except me.DoesNotExist:
            raise NotFoundException(
                {"error": f"Resource of id {obj_id} does not exist"}
            )
        except me.OperationError as error:
            raise OperationError([error.args[0]])

    def delete(self, obj_id: Union[int, str]):
        """
        delete an object matching the id
        :param obj_id: id of object to be deleted
        :return:
        """
        try:
            db_obj = self.model.objects.get(pk=obj_id)
            db_obj.delete()
            return True
        except me.DoesNotExist:
            raise NotFoundException(
                {"error": f"Resource of id {obj_id} does not exist"}
            )
        except me.OperationError as error:
            raise OperationError([error.args[0]])
