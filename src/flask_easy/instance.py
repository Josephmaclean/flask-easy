"""Main instance of application"""
import importlib
import importlib.util
import json
import os

from functools import cached_property
from flask import Flask, Response
from flask.typing import ResponseReturnValue
from flask_marshmallow import Marshmallow
from .exc.app_exceptions import AppExceptionCase, DBConnectionException
from .log import default_handler
from .database import Database
from flask_easy.scripts.cli import init_cli
from .response import ResponseEntity
from flasgger import Swagger

db = Database()
swag = Swagger()


class FlaskInstance(Flask):
    def make_response(self, response: ResponseReturnValue) -> Response:
        """
        Overwrite the base response class in order to use the ResponseEntity class
        see https://flask.palletsprojects.com/en/2.1.x/api/#flask.make_response for more info
        """
        if isinstance(response, ResponseEntity):
            schema = response.res_schema
            value = response.value
            many = response.many
            response = schema(many=many).dumps(value)
            return Response(response)
        return super().make_response(response)


class FlaskEasy:
    """
    Main class of flask easy. This initializes all the necessary/needed libraries so you don't have to do it yourself.
    """

    app: Flask

    def init_app(self, **kwargs) -> Flask:
        config = kwargs.pop("config")
        self.app = FlaskInstance(**kwargs)
        self.app.config.from_object(config)
        # if not app or not isinstance(app, Flask):
        #     raise TypeError("Invalid Flask application instance")

        # self.app = app

        # self.app.response_class = ApiResponse
        with self.app.app_context():
            self.app.logger.addHandler(default_handler)
            self._initialize_databases()
            self._handle_errors()
            self._register_blueprints()
            self._initialize_swagger()
            init_cli(self.app, db)

        return self.app

    def _handle_errors(self):
        @self.app.errorhandler(AppExceptionCase)
        def handle_app_exceptions(exc):
            return self.app_exception_handler(exc)

    def _initialize_databases(self):

        db_host = self.app.config.get("DB_HOST")
        db_name = self.app.config.get("DB_NAME")
        db_user = self.app.config.get("DB_USER")
        db_password = self.app.config.get("DB_PASSWORD")
        db_port = self.app.config.get("DB_PORT")
        db_engine = self.app.config.get("DB_ENGINE")
        if not db_engine:
            return

        db_engine = db_engine.lower()

        if db_engine == "mongodb":
            self._initialize_mongodb(db_host, db_name, db_password, db_port, db_user)
        else:
            db.init_app(self.app)

    def _initialize_mongodb(self, db_host, db_name, db_password, db_port, db_user):
        try:
            from flask_mongoengine import MongoEngine

            mongo_db_params = {
                "MONGODB_HOST": db_host,
                "MONGODB_DB": db_name,
                "MONGODB_PORT": int(db_port) if db_port else 27017,
                "MONGODB_USERNAME": db_user,
                "MONGODB_PASSWORD": db_password,
                "MONGODB_CONNECT": False,
            }
            self.app.config.from_mapping(**mongo_db_params)
            me = MongoEngine()
            me.init_app(self.app)
        except ImportError:
            msg = "'flask-mongoengine' package is required to connect to mongodb"
            raise ImportError(msg)

    def _initialize_sql(
        self, db_engine, db_host, db_name, db_password, db_port, db_user
    ):
        db_engine_port_map = {
            "postgres": ("postgresql+psycopg2", int(db_port) if db_port else 5432),
            "mysql": ("mysql+pymysql", int(db_port) if db_port else 3306),
            "sqlite": ("sqlite", None),
        }
        if db_engine not in db_engine_port_map:
            raise DBConnectionException(f"{db_engine} connection is not supported")
        db_details = db_engine_port_map.get(db_engine)
        engine_url_prefix = db_details[0]
        db_port = db_details[1]
        db_url = self.generate_db_url(
            engine_url_prefix, db_host, db_user, db_password, db_port, db_name
        )
        db.init_app(self.app)
        try:
            from flask_migrate import Migrate

            migrate = Migrate()
            migrate.init_app(self.app, db)
        except ImportError:
            raise ImportError("flask-migrate not installed")
        with self.app.app_context():
            db.create_all()
            ma = Marshmallow()
            ma.init_app(self.app)

    @cached_property
    def _urls(self):
        spec = importlib.util.spec_from_file_location(
            "urls", os.path.join(self.app.root_path, "urls.py")
        )
        urls = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(urls)
        return urls

    def _initialize_swagger(self):
        app_name = self.app.config.get("APP_NAME")
        self.app.config["SWAGGER"] = {"title": f"{app_name} API Docs", "uiversion": 3}
        swag.init_app(self.app)

    def _register_blueprints(self):
        """
        Register blueprints. Read from urls in project root path and register blueprints
        :return:
        """

        urls = self._urls
        urls.blueprints(self.app)

    @staticmethod
    def generate_db_url(
        engine_prefix, db_host, db_user, db_password, db_port, db_name
    ):  # noqa
        if engine_prefix == "sqlite":
            return f"sqlite:///{db_name}"

        return "{engine_prefix}://{db_user}:{password}@{host}:{port}/{db_name}".format(
            # noqa
            engine_prefix=engine_prefix,
            db_user=db_user,
            host=db_host,
            password=db_password,
            port=db_port,
            db_name=db_name,
        )

    @staticmethod
    def app_exception_handler(exc):
        return Response(
            json.dumps(exc.context),
            status=exc.status_code,
            mimetype="application/json",
        )
