import typing

import mongoengine
from pymongo.errors import ServerSelectionTimeoutError

from ..exc import OperationError, InternalServerError, NotFoundException
from .crud_repository_interface import CrudRepositoryInterface


class MongoRepository(CrudRepositoryInterface):
    model: mongoengine

    def index(self):
        """

        :return:
        """
        try:
            return self.model.objects()
        except mongoengine.OperationError:
            raise OperationError(message="Could not perform operation")

    def create(self, obj_data: dict):
        """

        :param obj_data:
        :return:
        """
        try:
            db_obj = self.model(**obj_data)
            db_obj.save()
            return db_obj
        except mongoengine.OperationError:
            raise OperationError(message="Could not perform operation")
        except ServerSelectionTimeoutError as e:
            raise InternalServerError(message=e.details)

    def update_by_id(self, obj_id: typing.Union[int, str], obj_in: dict):
        """

        :param obj_id:
        :param obj_in:
        :return:
        """
        try:
            db_obj = self.find_by_id(obj_id)
            db_obj.modify(**obj_in)
            return db_obj
        except mongoengine.OperationError:
            raise OperationError(message="Could not perform operation")
        except ServerSelectionTimeoutError as e:
            raise InternalServerError(message=e.details)

    def find(self, filter_param: dict):
        """
        returns an item that satisfies the data passed to it if it exists in
        the database

        :param filter_param: {dict}
        :return: model_object - Returns an instance object of the model passed
        """
        try:
            db_obj = self.model.objects.get(**filter_param)
            return db_obj
        except mongoengine.DoesNotExist:
            raise NotFoundException({"error": "Resource does not exist"})
        except mongoengine.OperationError:
            raise OperationError(message="Could not perform operation")

    def find_all(self, filter_param: dict):
        """
        returns all items that satisfies the filter params passed to it

        :param filter_param: {dict}
        :return: model_object - Returns an instance object of the model passed
        """
        db_obj = self.model.objects(**filter_param)
        return db_obj

    def find_by_id(self, obj_id: typing.Union[int, str]):
        try:
            db_obj = self.model.objects.get(pk=obj_id)
            return db_obj
        except mongoengine.DoesNotExist:
            raise NotFoundException(
                {"error": f"Resource of id {obj_id} does not exist"}
            )
        except mongoengine.OperationError:
            raise OperationError(message="Could not perform operation")
        except ServerSelectionTimeoutError as e:
            raise InternalServerError(message=e.details)

    def delete(self, obj_id: typing.Union[int, str]):
        """
        delete an object matching the query parameters
        :param obj_id: id of object to be deleted
        :return:
        """
        try:
            db_obj = self.model.objects.get(pk=obj_id)
            db_obj.delete()
            return True
        except mongoengine.DoesNotExist:
            raise NotFoundException(
                {"error": f"Resource of id {obj_id} does not exist"}
            )
        except mongoengine.OperationError:
            raise OperationError(message="Could not perform operation")
        except ServerSelectionTimeoutError as e:
            raise InternalServerError(message=e.details)
