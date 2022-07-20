"""
conftest.py

Author: Joseph Maclean Arhin
"""
import pytest
from flask_easy import FlaskEasy, db, fields
from flask_easy.repository.sql import Repository


class Config:
    APP_NAME = "My Awesome App"

    DATABASE = {"engine": "SqliteDatabase", "name": "example.db"}


@pytest.fixture
def create_app(config=Config()):
    """initialize flask easy"""
    app = FlaskEasy().init_app(**{"import_name": __name__, "config": config})
    return app


@pytest.fixture
def app_with_model(create_app):
    """initialize flask easy with User model created"""

    class User(db.Model):
        name = fields.CharField

    User.create_table()
    return User


@pytest.fixture
def app_with_repository(app_with_model):
    """initialize flask easy with User repository created"""

    class UserRepository(Repository):
        model = app_with_model

    return UserRepository
