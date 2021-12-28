from flask import current_app as app
from .sql_base_repository import SqlRepository
from .mongo_base_repository import MongoRepository
from ..extensions import db

class CrudRepository:
    def __new__(cls, *args, **kwargs):
        if app.config.get("DB_ENGINE", "").lower() == "mongodb":
            return super(CrudRepository, cls).__new__(MongoRepository, *args, **kwargs)
        else:
            instance = super(CrudRepository, cls).__new__(SqlRepository, *args, **kwargs)
            instance.db = db
            instance.model = None
            return instance


# class CrudRepository(BaseCrudRepository):
#     pass