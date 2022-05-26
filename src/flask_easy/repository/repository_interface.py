"""
repository_interface.py

Author: Joseph Maclean Arhin
"""
import abc
import typing as t

IdType = t.Union[int, str]


class RepositoryInterface(metaclass=abc.ABCMeta):
    """
    Base repository interface to be inherited by all repositories
    """

    @property
    def model(self):
        """
        the model that is bound to this repository. This model will be used for
        further queries and actions that will be done by the repository that
        inherits from this abstract class/interface mock
        """
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def index(cls):
        """
        when inherited, index should show all data belonging to a model
        :return: data
        """
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def create(cls, data: dict):
        """
        when inherited, creates a new record
        :param data: the data you want to use to create the model
        :return: data
        """
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def create_all(cls, data: t.List[dict]):
        """
        when inherited, creates new records
        :param data: the data you want to use to create the model
        :return: data
        """
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def update_by_id(cls, obj_id: IdType, data: dict):
        """
        when inherited, updates a record by taking in the id, and the data you
        want to update with
        :param obj_id:
        :param data:
        :return: a model object
        """

        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def find_by_id(cls, obj_id: IdType):
        """
        when inherited, finds a record by id
        :param obj_id:
        :return: a model object
        """

        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def find(cls, query_params: dict):
        """
        when inherited, should find a record by the parameters passed
        :param query_params:
        :return: a model object
        """

    @classmethod
    @abc.abstractmethod
    def find_all(cls, query_params: dict):
        """
        when inherited, should find all records by the parameters passed
        :param query_params:
        :return: a model object
        """

    @classmethod
    @abc.abstractmethod
    def delete(cls, obj_id: IdType):
        """
        takes in an id, finds and deletes the record
        :param obj_id:
        :return: model object
        """

        raise NotImplementedError
