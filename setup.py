from setuptools import setup

setup(
    name="Flask-Easy",
    install_requires=[
        "Flask==2.0.2",
        "marshmallow>=3.14.1",
        "blinker>=1.4",
        "flasgger>=0.9.5",
        "peewee>=3.14.0",
        "peewee-migrate>=1.4.8",
        "watchdog>=2.1.2",
        "cookiecutter>=1.7.3",
    ],
    entry_points={
        "console_scripts": ["easy-admin=flask_easy.scripts.easy_scripts:cli"]
    },
)
