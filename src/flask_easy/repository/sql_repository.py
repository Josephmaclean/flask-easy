from typing import Union, Optional, Type, List

from sqlalchemy.exc import DBAPIError

from ..exc import NotFoundException
from ..exc.app_exceptions import OperationError
from ..extensions import db
from .repository_interface import RepositoryInterface


class SqlRepository(RepositoryInterface):
    """
    Base class to be inherited by all repositories. This class comes with
    base crud functionalities attached
    """

    model: List[db.Model]

    def index(self) -> List[db.Model]:
        """
        :return: {list} returns a list of objects of type model
        """
        try:
            data = self.model.query.all()

            return data
        except DBAPIError as e:
            raise OperationError(message=e.orig.args[0])

    def create(self, data: dict) -> db.Model:
        """

        :param data: data to persist in the database
        :return: {Model} - Returns an instance object of the model passed
        """
        try:
            db_obj = self.model(**data)
            db.session.add(db_obj)
            db.session.commit()
            return db_obj
        except DBAPIError as e:
            raise OperationError(message=e.orig.args[0])

    def create_all(self, data: List[dict]):
        """
        Creates multiple objects from data provided
        :param data: List of data to persist in the database
        :return:
        """
        try:
            obj_list = [self.model(**item) for item in data]
            db.session.add_all(obj_list)
            db.session.commit()
        except DBAPIError as e:
            raise OperationError(message=e.orig.args[0])

    def update_by_id(self, obj_id: Union[int, str], data: dict) -> db.Model:
        """
        :param obj_id: {int}
        :param data: {dict}
        :return: model_object - Returns an instance object of the model passed
        """
        db_obj = self.find_by_id(obj_id)
        if not db_obj:
            raise NotFoundException(f"Resource of id {obj_id} does not exist")
        try:
            for field in data:
                if hasattr(db_obj, field):
                    setattr(db_obj, field, data[field])
            db.session.add(db_obj)
            db.session.commit()
            return db_obj
        except DBAPIError as e:
            raise OperationError(message=e.orig.args[0])

    def find_by_id(self, obj_id: int) -> db.Model:
        """
        returns an object if its id exists in the database
        :param obj_id: int - id of the user
        :return: model_object - Returns an instance object of the model passed
        """
        try:
            db_obj = self.model.query.get(obj_id)
            if db_obj is None:
                raise NotFoundException
            return db_obj
        except DBAPIError as e:
            raise OperationError(message=e.orig.args[0])

    def find(self, params: dict) -> db.Model:
        """
        find an object matching the query parameters
        :param params: filter parameters
        :return:
        """
        try:
            db_obj = self.model.query.filter_by(**params).first()
            return db_obj

        except DBAPIError as e:
            raise OperationError(message=e.orig.args[0])

    def find_all(self, query_params: dict) -> List[Optional[db.Model]]:
        """
        returns all items that satisfies the filter query_params passed to it

        :param query_params: query parameters to filter by
        :return: model_object - Returns an instance object of the model passed
        """
        try:
            db_obj = self.model.query.filter_by(**query_params).all()
            return db_obj
        except DBAPIError as e:
            raise OperationError(message=e.orig.args[0])

    def delete(self, obj_id: Union[int, str]) -> None:
        """
        delete an object matching the id
        :param obj_id: id of object to be deleted
        :return:
        """

        try:
            db_obj = self.find_by_id(obj_id)
            if not db_obj:
                raise NotFoundException
            db.session.delete(db_obj)
            db.session.commit()
        except DBAPIError as e:
            raise OperationError(message=e.orig.args[0])
