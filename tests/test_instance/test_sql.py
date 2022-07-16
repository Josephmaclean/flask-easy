from flask import Flask
from playhouse.test_utils import test_database
from flask_easy.database import Database


def test_sql_database():
    database = Database()
    flask = Flask(__name__)
    flask.config["DB_ENGINE"] = "sqlite"
    database.init_app(flask)
    assert True
