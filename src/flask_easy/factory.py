import importlib.util
import os
import sys

from importlib.machinery import SourceFileLoader
from flask import Flask

try:
    from faker import Faker
except ImportError as error:
    raise ImportError("faker is required to seed database")


def run_seeder(count, model, app: Flask):
    def _get_factory():
        path = os.path.join(app.root_path, "factory/__init__.py")
        spec = importlib.util.spec_from_loader("factory", SourceFileLoader("factory", path))
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)

    _get_factory()

    for _ in range(count):
        if model is None:
            for subclass in Seeder.__subclasses__():
                migrate(subclass)
        else:
            for subclass in Seeder.__subclasses__():
                if model.lower() == subclass.__name__.lower():
                    migrate(subclass)


def migrate(factory_class):
    fake = Faker()
    factory_class.fake = fake
    factory_class.run()


class Seeder:
    fake: Faker

    @classmethod
    def run(cls):
        raise NotImplementedError