from peewee import SqliteDatabase, MySQLDatabase, PostgresqlDatabase, Model as BaseModel
from playhouse.cockroachdb import CockroachDatabase
from flask import current_app

class Database:

    DB_ENGINE_MAP = {
        "postgres": (PostgresqlDatabase, 5432),
        "mysql": (MySQLDatabase, 3306),
        "sqlite": (SqliteDatabase, None),
        "cockroachdb": (CockroachDatabase, 26257)
    }

    def init_app(self, app):
        self.app = app
        self.database = self.load()
        self.register_handlers()
        self.Model = self.get_model()


    def initialize_sql(self, engine, name=None, user=None, password=None, host=None, port=None):
        db_engine, db_port = self.DB_ENGINE_MAP.get(engine)

        port = db_port if port is None else port
        return db_engine(name, user=user, password=password, host=host, port=port)

    def load(self):
        config = self.app.config
        engine = config.get("DB_ENGINE")
        user = config.get("DB_USER")
        password = config.get("DB_PASSWORD")
        host = config.get("DB_HOST")
        name = config.get("DB_NAME")
        port = config.get("DB_PORT")
        return self.initialize_sql(engine=engine, user=user, password=password, host=host, port=port, name=name)

    def get_model(self):
        class DataModel(BaseModel):
            class Meta:
                database = self.database

        return DataModel

    def connect_db(self):
        if self.database.is_closed():
            self.database.connect()

    def close_db(self, exc):
        if not self.database.is_closed():
            self.database.close()

    def register_handlers(self):
        self.app.before_request(self.connect_db)
        self.app.teardown_request(self.close_db)
