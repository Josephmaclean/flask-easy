"""
Repositories

This module aggregates submodules. Import repositories from here
"""

from flask import current_app

from .mongo_repository import MongoRepository
from .peewee_sql_repository import PeeweeSqlRepository as SqlRepository
