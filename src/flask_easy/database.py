"""
database.py

Author: Joseph Maclean Arhin
"""
from flask import Flask
from peewee import SqliteDatabase, MySQLDatabase, PostgresqlDatabase, Model as BaseModel
from playhouse.cockroachdb import CockroachDatabase


class Database:
    """
    base database class for peewee connection
    """

    DB_ENGINE_MAP = {
        "postgres": (PostgresqlDatabase, 5432),
        "mysql": (MySQLDatabase, 3306),
        "sqlite": (SqliteDatabase, None),
        "cockroachdb": (CockroachDatabase, 26257),
    }
    app: Flask
    Model = None
    database = None

    def init_app(self, app):
        """initialize peewee"""
        self.app = app
        self.database = self.load()
        self.register_handlers()
        self.Model = self.get_model()  # pylint: disable=C0103

    def initialize_sql(  # pylint: disable=R0913
        self, engine, name=None, user=None, password=None, host=None, port=None
    ):
        """initialize database connection"""
        db_engine, db_port = self.DB_ENGINE_MAP.get(engine)

        port = db_port if port is None else port
        return db_engine(name, user=user, password=password, host=host, port=port)

    def load(self):
        """load database"""
        config = self.app.config
        engine = config["DB_ENGINE"]
        user = config.get("DB_USER")
        password = config.get("DB_PASSWORD")
        host = config.get("DB_HOST")
        name = config.get("DB_NAME")
        port = config.get("DB_PORT")
        return self.initialize_sql(
            engine=engine, user=user, password=password, host=host, port=port, name=name
        )

    def get_model(self):
        """Generate model class"""

        class DataModel(BaseModel):
            """DataModel to be extended by all other sql models"""

            class Meta:  # pylint: disable=R0903
                """Meta class"""

                database = self.database

        return DataModel

    def connect_db(self):
        """connect to database"""
        if self.database.is_closed():
            self.database.connect()

    def close_connection(self, *args, **kwargs):  # pylint: disable=W0613
        """close database connection"""
        if not self.database.is_closed():
            self.database.close()

    def register_handlers(self):
        """register database connectors"""
        self.app.before_request(self.connect_db)
        self.app.teardown_request(self.close_connection)
