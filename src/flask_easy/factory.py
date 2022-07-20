"""
factory.py

Author: Joseph Maclean Arhin
"""
import importlib.util
import os
import sys

from importlib.machinery import SourceFileLoader
from flask import Flask

from faker import Faker


def run_seeder(count, model, app: Flask):
    """
    Run database seeder
    :param count: The number of times you want to seed
    :param model: The model
    :param app: Flask app
    :return:
    """

    def _get_factory():
        path = os.path.join(app.root_path, "factory/__init__.py")
        spec = importlib.util.spec_from_loader(
            "factory", SourceFileLoader("factory", path)
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)

    _get_factory()
    # db.connect_db()
    # get_subclasses()

    for _ in range(count):
        if model is None:
            for subclass in Seeder.__subclasses__():
                seed(subclass)
        else:
            for subclass in Seeder.__subclasses__():
                if model.lower() == subclass.__name__.lower():
                    seed(subclass)


def seed(factory_class):
    """
    Run the seeding action
    :param factory_class: The db seeder class
    :return:
    """

    fake = Faker()
    factory_class.fake = fake
    factory_class.run()


class Seeder:  # pylint: disable=R0903
    """Root seeder class to be inherited when creating a database seeder"""

    fake: Faker

    @classmethod
    def run(cls):
        """Logic to be run is goes here. This includes the database insert logic"""
        raise NotImplementedError
