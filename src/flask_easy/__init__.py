from .instance import FlaskEasy, db, swag, Flask
from .validator import validator
from .result import ServiceResult, handle_result
import peewee as fields
from flask import *
from .response import ResponseEntity
import flasgger as swagger

__version__ = "0.0.2"
