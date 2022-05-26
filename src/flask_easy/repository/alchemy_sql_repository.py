# import typing as t
#
# from sqlalchemy.exc import DBAPIError
#
# from ..exc import NotFoundException
# from ..exc.app_exceptions import OperationError
# from ..extensions import db
# from .repository_interface import RepositoryInterface
#
#
# class AlchemySqlRepository(RepositoryInterface):
#     """
#     Base class to be inherited by all repositories. This class comes with
#     base crud functionalities attached
#     """
#
#     model: t.Type[db.Model]
#
#     def __new__(cls, *args, **kwargs):
#         obj = super().__new__(cls, *args, **kwargs)
#         obj.db = db
#         return obj
#
#     def index(self) -> t.List[db.Model]:
#         """
#         :return: {list} returns a list of objects of type model
#         """
#         try:
#             data = self.model.query.all()
#
#             return data
#         except DBAPIError as error:
#             raise OperationError(message=error.orig.args[0]) from error
#
#     def create(self, data: dict) -> db.Model:
#         """
#
#         :param data: data to persist in the database
#         :return: {Model} - Returns an instance object of the model passed
#         """
#         try:
#             db_obj = self.model(**data)
#             self.db.session.add(db_obj)
#             self.db.session.commit()
#             return db_obj
#         except DBAPIError as error:
#             raise OperationError(message=error.orig.args[0]) from error
#
#     def create_all(self, data: t.List[dict]):
#         """
#         Creates multiple objects from data provided
#         :param data: List of data to persist in the database
#         :return:
#         """
#         try:
#             obj_list = [self.model(**item) for item in data]
#             self.db.session.add_all(obj_list)
#             self.db.session.commit()
#         except DBAPIError as error:
#             raise OperationError(message=error.orig.args[0]) from error
#
#     def update_by_id(self, obj_id: t.Union[int, str], data: dict) -> db.Model:
#         """
#         :param obj_id: {int}
#         :param data: {dict}
#         :return: model_object - Returns an instance object of the model passed
#         """
#         db_obj = self.find_by_id(obj_id)
#         if not db_obj:
#             raise NotFoundException(f"Resource of id {obj_id} does not exist")
#         try:
#             for field in data:
#                 if hasattr(db_obj, field):
#                     setattr(db_obj, field, data[field])
#             self.db.session.add(db_obj)
#             self.db.session.commit()
#             return db_obj
#         except DBAPIError as error:
#             raise OperationError(message=error.orig.args[0]) from error
#
#     def find_by_id(self, obj_id: int) -> db.Model:
#         """
#         returns an object if its id exists in the database
#         :param obj_id: int - id of the user
#         :return: model_object - Returns an instance object of the model passed
#         """
#         try:
#             db_obj = self.model.query.get(obj_id)
#             if db_obj is None:
#                 raise NotFoundException
#             return db_obj
#         except DBAPIError as error:
#             raise OperationError(message=error.orig.args[0]) from error
#
#     def find(self, params: dict) -> db.Model:
#         """
#         find an object matching the query parameters
#         :param params: filter parameters
#         :return:
#         """
#         try:
#             db_obj = self.model.query.filter_by(**params).first()
#             return db_obj
#
#         except DBAPIError as error:
#             raise OperationError(message=error.orig.args[0]) from error
#
#     def find_all(self, query_params: dict) -> t.List[t.Optional[db.Model]]:
#         """
#         returns all items that satisfies the filter query_params passed to it
#
#         :param query_params: query parameters to filter by
#         :return: model_object - Returns an instance object of the model passed
#         """
#         try:
#             db_obj = self.model.query.filter_by(**query_params).all()
#             return db_obj
#         except DBAPIError as error:
#             raise OperationError(message=error.orig.args[0]) from error
#
#     def delete(self, obj_id: t.Union[int, str]) -> None:
#         """
#         delete an object matching the id
#         :param obj_id: id of object to be deleted
#         :return:
#         """
#
#         try:
#             db_obj = self.find_by_id(obj_id)
#             if not db_obj:
#                 raise NotFoundException
#             self.db.session.delete(db_obj)
#             self.db.session.commit()
#         except DBAPIError as error:
#             raise OperationError(message=error.orig.args[0]) from error
