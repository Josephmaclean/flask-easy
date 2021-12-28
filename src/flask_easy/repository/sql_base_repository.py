import typing
from typing import Union, List, Optional

from sqlalchemy.exc import DBAPIError, IntegrityError

from ..exc import NotFoundException
from ..exc.app_exceptions import OperationError
from ..extensions import db
from .crud_repository_interface import CrudRepositoryInterface


class SqlRepository(CrudRepositoryInterface):
    model: db.Model

    def __init__(self):
        """
        Base class to be inherited by all repositories. This class comes with
        base crud functionalities attached

        :param model: base model of the class to be used for queries
        """

        self.db = db

    def index(self) -> List[db.Model]:
        """
        :return: {list} returns a list of objects of type model
        """
        try:
            data = self.model.query.all()

            return data
        except DBAPIError as e:
            raise OperationError(message=e.orig.args[0])

    def create(self, obj_data: dict) -> db.Model:
        """

        :param obj_in: the data you want to use to create the model
        :return: {object} - Returns an instance object of the model passed
        """
        try:
            db_obj = self.model(**obj_data)
            self.db.session.add(db_obj)
            self.db.session.commit()
            return db_obj
        except DBAPIError as e:
            raise OperationError(message=e.orig.args[0])

    def create_all(self, data: List[dict]) -> List[db.Model]:

        try:
            obj_list = [self.model(**item) for item in data]
            self.db.session.add_all(obj_list)
            self.db.session.commit()
        except DBAPIError as e:
            raise OperationError(message=e.orig.args[0])

    def update_by_id(self, obj_id: Union[int, str], obj_in: dict) -> db.Model:
        """
        :param obj_id: {int}
        :param obj_in: {dict}
        :return: model_object - Returns an instance object of the model passed
        """
        db_obj = self.find_by_id(obj_id)
        if not db_obj:
            raise NotFoundException(f"Resource of id {obj_id} does not exist")
        try:
            for field in obj_in:
                if hasattr(db_obj, field):
                    setattr(db_obj, field, obj_in[field])
            self.db.session.add(db_obj)
            self.db.session.commit()
            return db_obj
        except DBAPIError as e:
            raise OperationError(message=e.orig.args[0])

    def find_by_id(self, obj_id: int) -> db.Model:
        """
        returns a user if it exists in the database
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

    def find_all(self, params: dict) -> List[Optional[db.Model]]:
        """
        find all object matching the query parameters
        :param params: filter parameters
        :return:
        """
        try:
            db_obj = self.model.query.filter_by(**params).all()
            return db_obj
        except DBAPIError as e:
            raise OperationError(message=e.orig.args[0])

    def delete(self, obj_id: Union[int, str]) -> None:
        """
        delete an object matching the query parameters
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
