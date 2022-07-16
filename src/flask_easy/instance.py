"""
instance.py

Author: Joseph Maclean Arhin
"""
import importlib
import importlib.util
import json
import os
import typing as t

from collections import namedtuple

from functools import cached_property
from flasgger import Swagger
from flask import Flask, Response
from flask.typing import ResponseReturnValue
from flask_easy.scripts.cli import init_cli
from .exc.app_exceptions import AppExceptionCase
from .database import Database
from .response import ResponseEntity
from .security import authenticator, TokenDecoder

db = Database()
swag = Swagger()

Route = namedtuple("Route", "view url_prefix", defaults=[None])


class FlaskInstance(Flask):
    """
    Flask Instance
    """

    def make_response(self, rv: ResponseReturnValue) -> Response:
        """
        Overwrite the base response class in order to use the ResponseEntity class
        see https://flask.palletsprojects.com/en/2.1.x/api/#flask.make_response for more info
        """
        if isinstance(rv, ResponseEntity):
            values = rv.values
            schema = values["schema"]
            value = values["value"]
            many = values["many"]
            status = values["status"]
            mimetype = values["mimetype"]
            if schema:
                response = schema(many=many).dumps(value)
                mimetype = "application/json"
            else:
                response = value
            return Response(response, status=status, mimetype=mimetype)
        return super().make_response(rv)


class FlaskEasy:
    """
    Main class of flask easy. This initializes all the necessary/needed libraries
    """

    app: Flask

    def init_app(self, **kwargs) -> Flask:
        """
        initialize flask easy
        :param kwargs:
        :return:
        """
        config = kwargs.pop("config")
        self.app = FlaskInstance(**kwargs)
        self.app.config.from_object(config)
        with self.app.app_context():
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
        """
        Initialize databases based on engine selection
        :return:
        """

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

    def _initialize_mongodb(
        self, db_host, db_name, db_password, db_port, db_user
    ):  # pylint: disable=R0913
        try:
            from flask_mongoengine import MongoEngine  # pylint: disable=C0415

            self.app.config["MONGODB_SETTINGS"] = {
                "host": db_host,
                "db": db_name,
                "username": db_user,
                "password": db_password,
                "port": int(db_port) if db_port else 27017,
            }
            mongo_engine = MongoEngine()
            mongo_engine.init_app(self.app)
        except ImportError as error:
            msg = "'flask-mongoengine' package is required to connect to mongodb"
            raise ImportError(msg) from error

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

        routes: t.List[Route] = self._urls.routes
        for url_route in routes:
            self.app.register_blueprint(url_route.view, url_prefix=url_route.url_prefix)

    @staticmethod
    def generate_db_url(
        engine_prefix,
        db_host,
        db_user,
        db_password,
        db_port,
        db_name,
    ):  # pylint: disable=R0913
        """
        generate database connection string
        :param engine_prefix:
        :param db_host:
        :param db_user:
        :param db_password:
        :param db_port:
        :param db_name:
        :return:
        """
        if engine_prefix == "sqlite":
            return f"sqlite:///{db_name}"

        return (
            f"{engine_prefix}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )

    @staticmethod
    def app_exception_handler(exc):
        """
        handle unhandled exceptions
        :param exc:
        :return:
        """
        return Response(
            json.dumps(exc.context),
            status=exc.status_code,  # pylint: disable=w0212
            mimetype="application/json",
        )

    @staticmethod
    def register_auth(auth_class: t.Type[TokenDecoder]):
        """
        Register authentication handlers
        :param auth_class:
        :return:
        """
        authenticator.register_token_decoder(auth_class)
