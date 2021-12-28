"""All external flask extensions used flask-easy"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_apispec import FlaskApiSpec


db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
docs = FlaskApiSpec(document_options=False)
