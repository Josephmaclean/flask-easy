import pytest
from flask import Flask
from flask_easy import FlaskEasy
import mongoengine as me


class Config:
    APP_NAME = "My Awesome App"

    # DB_HOST = "127.0.0.1"
    # DB_USER = "maclean"
    # DB_NAME = "cv_parser"
    # DB_PASSWORD = "camaro"
    DB_ENGINE = "sqlite"


@pytest.fixture
def create_app(config=Config()):
    app = FlaskEasy().init_app(**{"import_name": __name__, "config": config})
    return app


# class MyModel(me.Document):
#     title = me.StringField()


def test_initialization(create_app):
    # connection = MongoEngine.connection
    # model = MyModel(title="hello").save()
    print(model)
