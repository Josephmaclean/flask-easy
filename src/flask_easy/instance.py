"""Main instance of application"""
import importlib
import importlib.util
import typing
import os

from functools import cached_property
from flask import Flask
from flask_mongoengine import MongoEngine

from .exc.app_exceptions import AppExceptionCase, HTTPException
from .exc.handler import app_exception_handler
from .exc.setup_exceptions import DBConnectionException
from .extensions import ma, migrate, db, docs
from .generators import init_generators
from .log import default_handler


class FlaskEasy:
    app: Flask

    def init_app(self, app: Flask) -> None:
        if not app or not isinstance(app, Flask):
            raise TypeError("Invalid Flask application instance")

        self.app = app
        with app.app_context():
            app.logger.addHandler(default_handler)
            self._register_extensions(app)
            self._register_blueprints()
            self.register_apispec(app)
        return app

    def _register_extensions(self, flask_app: Flask):
        """Register flask extensions"""

        self.initialize_databases(flask_app)

        init_generators(flask_app)

        @flask_app.errorhandler(HTTPException)
        def handle_http_exception(exc: Exception):
            return app_exception_handler(exc)

        @flask_app.errorhandler(AppExceptionCase)
        def handle_app_exceptions(exc):
            return app_exception_handler(exc)

    def initialize_databases(self, flask_app: Flask):
        app = flask_app

        db_host = app.config.get("DB_HOST")
        db_name = app.config.get("DB_NAME")
        db_user = app.config.get("DB_USER")
        db_password = app.config.get("DB_PASSWORD")
        db_port = app.config.get("DB_PORT")
        db_engine = app.config.get("DB_ENGINE")
        if not db_engine:
            return

        db_engine = db_engine.lower()

        if db_engine == "mongodb":
            mongo_db_params = {
                "MONGODB_DB": db_name,
                "MONGODB_PORT": int(db_port) if db_port else 27017,
                "MONGODB_USERNAME": db_user,
                "MONGODB_PASSWORD": db_password,
                "MONGODB_CONNECT": False,
            }
            app.config.from_mapping(**mongo_db_params)
            me = MongoEngine()
            me.init_app(flask_app)

        else:
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

            app.config.from_mapping(SQLALCHEMY_DATABASE_URI=db_url)
            app.config.from_mapping(SQLALCHEMY_TRACK_MODIFICATIONS=True)
            db.init_app(flask_app)
            migrate.init_app(flask_app, db)
            with flask_app.app_context():
                db.create_all()
                ma.init_app(flask_app)

    @cached_property
    def _urls(self):
        spec = importlib.util.spec_from_file_location("urls",  os.path.join(self.app.root_path, "urls.py"))
        urls = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(urls)
        return urls

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
    def register_apispec(app):
        docs.init_app(app)
        for name, rule in app.view_functions.items():
            try:
                blueprint_name, _ = name.split('.')
            except ValueError:
                blueprint_name = None

            if blueprint_name:
                try:
                    docs.register(rule, blueprint=blueprint_name)
                except TypeError:
                    pass

