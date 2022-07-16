"""
setup.py

Author: Joseph Maclean Arhin
"""
from setuptools import setup

setup(
    name="Flask-Easy",
    install_requires=[
        "Flask>=2.1.3",
        "marshmallow>=3.14.1",
        "blinker>=1.4",
        "flasgger>=0.9.5",
        "peewee>=3.14.0",
        "peewee-migrate>=1.4.8",
        "watchdog>=2.1.2",
        "cookiecutter>=1.7.3",
        "apispec>=5.2.2",
        "faker>=13.12.0",
    ],
    entry_points={
        "console_scripts": ["easy-admin=flask_easy.scripts.easy_scripts:cli"]
    },
)
