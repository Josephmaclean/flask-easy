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
from playhouse.flask_utils import FlaskDB

from flask_easy.scripts.cli import init_cli
from .exc.app_exceptions import AppExceptionCase
from .response import ResponseEntity
from .security import authenticator, TokenDecoder

db = FlaskDB()
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
        database_param = self.app.config.get("DATABASE")
        if not database_param:
            return

        db_engine = database_param.get("engine")
        if db_engine == "mongodb":
            self._initialize_mongodb(**database_param)
        else:
            db.init_app(self.app)

    def _initialize_mongodb(self, **kwargs):  # pylint: disable=R0913
        try:
            from flask_mongoengine import MongoEngine  # pylint: disable=C0415

            kwargs.pop("engine")
            kwargs["username"] = kwargs.pop("user")
            kwargs["db"] = kwargs.get("name")
            self.app.config["MONGODB_SETTINGS"] = kwargs
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
