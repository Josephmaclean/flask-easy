"""
conftest.py

Author: Joseph Maclean Arhin
"""
import pytest
from flask_easy import FlaskEasy, db, fields
from flask_easy.repository.sql import Repository


class Config:  # pylint: disable=R0903
    """Configuration for app setup"""

    APP_NAME = "My Awesome App"

    DATABASE = {"engine": "SqliteDatabase", "name": ":memory"}


@pytest.fixture
def create_app(config=Config()):
    """initialize flask easy"""
    app = FlaskEasy().init_app(**{"import_name": __name__, "config": config})
    return app


@pytest.fixture
def app_with_model(create_app):  # pylint: disable=W0621 disable=W0613
    """initialize flask easy with User model created"""

    class User(db.Model):
        """User model for test"""

        name = fields.CharField()

    User.create_table()
    yield User

    User.drop_table()


@pytest.fixture
def app_with_repository(app_with_model):  # pylint: disable=W0621
    """initialize flask easy with User repository created"""

    class UserRepository(Repository):
        """User repository for test"""

        model = app_with_model

    yield UserRepository

    app_with_model.drop_table()
