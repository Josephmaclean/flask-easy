# FLASK EASY
Flask easy is a battery included framework built on top of flask that helps with easy project scaffolding and project setup. Taking inspirations from other frameworks such as Django, SpringBoot and Laravel, flask-easy takes care of setting up your flask application with all the necessary dependencies, structure so that all you need to think of is churn out your precious features.

## Installation

    pip install flask-easy

## Getting Started
Once installed, run the scaffolding command and follow the prompt by selecting your desired setup
```
easy-admin scaffold <project-path>
```

When the command is run, the project will be spawned in the specified directory with the directory structure below

## Directory Structure

```
├── app
│   ├── __init__.py
│   ├── models
│   │   ├── README.md
│   │   └── __init__.py
│   ├── repositories
│   │   ├── README.md
│   │   └── __init__.py
│   ├── schemas
│   │   ├── README.md
│   │   └── __init__.py
│   ├── services
│   │   ├── README.md
│   │   └── __init__.py
│   ├── urls.py
│   └── views
│       ├── README.md
│       └── __init__.py
├── config.py
└── tests
    └── __init__.py

```

### app
This contains the main app. This in addition to the config.py file is what will be deployed in production

#### app/__init__.py
This file contains all main instance of your app. This is the entry point to the project

### models
Battery included directory. This is where your models should be.
All models generated using the `flask easy generate model <model_name>` command will be spawned in this directory and
automatically imported in the `__init__.py` file here

The snippets below are sample codes generated for sql and mongodb respectively using the `generate model` command
```python
# SQL
from flask_easy import db, fields


class User(db.Model):
    pass

```

```python
# Mongodb
import mongoengine as me


class User(me.Document):
    id = me.IntField(primary_key=True)
   ```


### repositories
Battery included directory. This is where your repositories should be. We advise that you extract all database logic
into this directory. You can also inherit from Repository classes that take care of basic queries so you don't have to
do it yourself. These classes can be overridden.

Repositories generate generated using the `flask easy generate repository <repository_name>` command will be spawned in this directory and
automatically imported in the `__init__.py` file here

The snippets below are sample codes generated for sql and mongodb respectively using the `generate repository `command

```python
# note that this is for sql

from flask_easy.repository.sql import Repository
from app.models import User


class UserRepository(Repository):
    model = User

    # other peewee sql query logic goes here


```

```python
# for mongodb

from flask_easy.repository.mongo import Repository
from app.models import User


class UserRepository(Repository):
    model = User

    # Other mongengine query logic goes here

```

### schemas
Not battery included. The `schemas` directory contains all your marshmallow schema for validating,
serializing and deserializing your data

### services
Not battery included. The `services` directory contains all your business logic. This directory can be deleted but it
is advised that you keep your business logic here for clean code

### tests
This directory contains all your test cases. This is where your tests should be.

# Features

## Routing
Flask easy is built on top of flask as it's name suggests so routing is basically the same with one caveat ``urls.py``
#### urls.py
When a project is generated, it is accompanied by a urls.py file.

```python
from flask_easy import route

routes = []
```
This is where you register all your views/blueprints.

e.g

```python
# views/user_view.py
from flask_easy import ResponseEntity, Blueprint

user = Blueprint("user", __name__)


@user.get("/user/hello")
def hello_user():
    return ResponseEntity.ok({"greeting": "hello"})

```


```python
# urls.py

from flask_easy import Route
from app.views import user # Note that user is a blueprint
from app.views import otherview

routes = [
    Route(user),
    Route(otherview, url_prefix="api/v1/example") # add url prefixes to all routes in this view
]
```

## Config.py
Whenever a new project is spawned using the `easy-admin scaffold <path>` command, a new `config.py` file is created in addition.
This file is created for configuration handling as described in the [flask documentation](https://flask.palletsprojects.com/en/2.1.x/config/).

```python
class Config:
    APP_NAME = "My Awesome App"

    DB_HOST = ""
    DB_USER = ""
    DB_NAME = ""
    DB_PASSWORD = ""
    DB_ENGINE = "postgres"


class DevelopmentConfig(Config):
    pass


class ProductionConfig(Config):
    pass


class TestingConfig(Config):
    pass

 ```

With the database connections already taken care for you, it's important to make sure that your database preference
and credentials are set properly. You can change your database using the `DB_ENGINE` variable. Below are a list of the supported databases

1. postgres
2. sqlite
3. mysql
4. mongodb

The `APP_NAME` variable should be changed to your preferred name. This will also reflect in Swagger UI


## Database Support
Flask-Easy banks on [Peewee ORM](http://docs.peewee-orm.com/en/latest/) and [MongoEngine ODM](http://mongoengine.org/)
for database connectivity and support and has a thin wrapper around these packages just to take off the stress of setting
your database up from your shoulders. Although you can select your database when scaffolding your app, you can change it
at anytime in the `config.py` file.

### Migration(SQL Only)
1. Make migration: `flask easy make:migration`
2. Migrate database: `flask easy migrate`
3. Rollback database migration: `flask easy migrate:rollback`

All migrations are taken care of by the Peewee library.

## Authentication & Authorization
Flask easy provides a mechanism for you to easily authenticate and authorize your routes.

## Seeding
Flask easy provides an inbuilt mechanism for you to easily seed your databases with dummy data for easier and faster
testing.

```python
# models/job.py

import uuid
import mongoengine as me


class Job(me.Document):
    id = me.UUIDField(default=uuid.uuid4, primary_key=True)
    title = me.StringField()
    summary = me.StringField()
    requirements = me.ListField()
    skills = me.ListField()

```
```python
# factory/job_seeder.py

from flask_easy.factory import Seeder
from app.models import Job


class JobSeeder(Seeder):
    @classmethod
    def run(cls):
        job = Job(
            title=cls.fake.name(),
            summary=cls.fake.sentence(),
            requirements=[cls.fake.sentence()],
            skills=[cls.fake.sentence()],

        )
        job.save()

```
with the help of the command `flask easy db:seed --class_name=JobSeeder`, you can seed your database with the data you need.
To seed the database 10 times is as easy as `flask easy db:seed 10 --class_name=JobSeeder`


## Swagger UI
Flask Easy comes with swagger UI integrated with the help of the excellent [flasgger library](https://github.com/flasgger/flasgger)
All the documentation required on its usage is available [here](https://github.com/flasgger/flasgger)
