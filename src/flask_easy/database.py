# """
# database.py
#
# Author: Joseph Maclean Arhin
# """
# import sys
# import typing as t
# from flask import Flask
# from peewee import  Model as BaseModel
#
#
# class Database:
#     """
#     base database class for peewee connection
#     """
#
#     # DB_ENGINE_MAP = {
#     #     "postgres": (PostgresqlDatabase, 5432),
#     #     "mysql": (MySQLDatabase, 3306),
#     #     "sqlite": (SqliteDatabase, None),
#     #     "cockroachdb": (CockroachDatabase, 26257),
#     # }
#     app: Flask
#     Model = None
#     database = None
#
#     def init_app(self, app):
#         """initialize peewee"""
#         self.app = app
#         self.database = self.load()
#         self.register_handlers()
#         self.Model = self.get_model()
#         # pylint: disable=C0103
#
#     def initialize_sql(  # pylint: disable=R0913
#         self, engine, name=None, **kwargs
#     ):
#         """initialize database connection"""
#         db_engine = getattr(sys.modules['peewee'], engine)
#
#         if engine == 'SqliteDatabase':
#             database = db_engine(
#                 name)
#             # database.connect()
#             return database
#         return db_engine(name, **kwargs)
#
#     def load(self):
#         """load database"""
#         config = self.app.config.pop("DATABASE")
#         return self.initialize_sql(
#             **config
#         )
#
#     def get_model(self):
#         """Generate model class"""
#
#         class DataModel(BaseModel):
#             """DataModel to be extended by all other sql models"""
#
#             class Meta:  # pylint: disable=R0903
#                 """Meta class"""
#
#                 database = self.database
#
#         return DataModel
#
#     def connect_db(self):
#         """connect to database"""
#         if self.database.is_closed():
#             self.database.connect()
#
#     def close_connection(self, *args, **kwargs):  # pylint: disable=W0613
#         """close database connection"""
#         if not self.database.is_closed():
#             self.database.close()
#
#     def register_handlers(self):
#         """register database connectors"""
#         self.app.before_request(self.connect_db)
#         self.app.teardown_request(self.close_connection)
#
#     def create_tables(self, tables: t.List[Model]):
#         with self.database:
#             self.database.create_tables(tables)
