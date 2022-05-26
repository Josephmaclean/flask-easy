"""
__init__.py

Author: Joseph Maclean Arhin
"""

import peewee as fields
from flask import *
import flasgger as swagger
import marshmallow as schema
from .instance import FlaskEasy, db, swag
from .validator import validator
from .response import ResponseEntity


__version__ = "0.0.2"
