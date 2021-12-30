"""
Repository Interface
"""
import abc
from typing import List, Union

IdType = Union[int, str]


class RepositoryInterface(metaclass=abc.ABCMeta):
    @property
    def model(self):
        """
        the model that is bound to this repository. This model will be used for
        further queries and actions that will be done by the repository that
        inherits from this abstract class/interface mock
        """
        raise NotImplementedError

    @abc.abstractmethod
    def index(self):
        """
        when inherited, index should show all data belonging to a model
        :return: data
        """
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, data: dict):
        """
        when inherited, creates a new record
        :param data: the data you want to use to create the model
        :return: data
        """
        raise NotImplementedError

    @abc.abstractmethod
    def create_all(self, data: List[dict]):
        """
        when inherited, creates new records
        :param data: the data you want to use to create the model
        :return: data
        """
        raise NotImplementedError

    @abc.abstractmethod
    def update_by_id(self, obj_id: IdType, data: dict):
        """
        when inherited, updates a record by taking in the id, and the data you
        want to update with
        :param obj_id:
        :param data:
        :return: a model object
        """

        raise NotImplementedError

    @abc.abstractmethod
    def find_by_id(self, obj_id: IdType):
        """
        when inherited, finds a record by id
        :param obj_id:
        :return: a model object
        """

        raise NotImplementedError

    @abc.abstractmethod
    def find(self, query_params: dict):
        """
        when inherited, should find a record by the parameters passed
        :param query_params:
        :return: a model object
        """

    @abc.abstractmethod
    def find_all(self, query_params: dict):
        """
        when inherited, should find all records by the parameters passed
        :param query_params:
        :return: a model object
        """

    @abc.abstractmethod
    def delete(self, obj_id: IdType):
        """
        takes in an id, finds and deletes the record
        :param obj_id:
        :return: model object
        """

        raise NotImplementedError
