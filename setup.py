from setuptools import setup, find_packages

setup(
    name="Flask-Easy",
    install_requires=[
        "Flask==2.0.2",
        "Flask-SQLAlchemy>=2.5.1",
        "Flask-Migrate>=3.1.0",
        "flask-marshmallow>=0.14.0",
        "flasgger>=0.9.5",
    ],
)
