"""Main instance of application"""
import importlib
import importlib.util
import json
import os

from functools import cached_property
from flask import Flask, Response
from flask_marshmallow import Marshmallow

from .exc.app_exceptions import AppExceptionCase, DBConnectionException
from .extensions import db
from .log import default_handler


class FlaskEasy:
    app: Flask

    def init_app(self, app: Flask) -> Flask:
        if not app or not isinstance(app, Flask):
            raise TypeError("Invalid Flask application instance")

        self.app = app
        with app.app_context():
            app.logger.addHandler(default_handler)
            self._initialize_databases()
            self._handle_errors()
            self._register_blueprints()
            self._initialize_swagger()

        return app

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
            self._initialize_sql(
                db_engine, db_host, db_name, db_password, db_port, db_user
            )

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
            "oracle": ("oracle+cx_oracle", int(db_port) if db_port else 1521),
            "mssql": ("mssql+pymssql", int(db_port) if db_port else 1433),
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
        self.app.config.from_mapping(SQLALCHEMY_DATABASE_URI=db_url)
        self.app.config.from_mapping(SQLALCHEMY_TRACK_MODIFICATIONS=True)
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
        try:
            from flasgger import Swagger

            swagger = Swagger()
            swagger.init_app(self.app)
        except ImportError:
            raise ImportError("Flasgger not installed")

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
            json.dumps(
                {"app_exception": exc.exception_case, "errorMessage": exc.context}
            ),
            status=exc.status_code,
            mimetype="application/json",
        )
