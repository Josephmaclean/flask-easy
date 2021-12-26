import abc
import typing

IdType = typing.Union[int, str]


class CrudRepositoryInterface(metaclass=abc.ABCMeta):
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
        :return: obj_data
        """
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, obj_data: typing.Dict):
        """
        when inherited, creates a new record
        :param obj_data: the data you want to use to create the model
        :return: obj_data
        """
        raise NotImplementedError

    @abc.abstractmethod
    def update_by_id(self, obj_id: IdType, obj_in: typing.Dict):
        """
        when inherited, updates a record by taking in the id, and the data you
        want to update with
        :param obj_id:
        :param obj_in:
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
    def find(self, obj_data: typing.Dict):
        """
        when inherited, should find a record by the parameters passed
        :param obj_data:
        :return: a model object
        """

    @abc.abstractmethod
    def find_all(self, data: typing.Dict):
        """
        when inherited, should find all records by the parameters passed
        :param obj_data:
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
