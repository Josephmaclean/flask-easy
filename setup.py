from setuptools import setup, find_packages

setup(
    name="Flask-Easy",
    install_requires=[
        "Flask==2.0.2",
        "Flask-SQLAlchemy>=2.5.1",
        "Flask-Migrate>=3.1.0",
        "flask-mongoengine>=1.0.0",
        "flask-marshmallow>=0.14.0",
        "apispec==5.0.0",
        "flask-apispec==0.11.0"
    ],
)
