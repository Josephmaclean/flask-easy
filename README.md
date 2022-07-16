# FLASK EASY
Flask easy is a battery included framework built on top of flask that helps with easy project scaffolding and project setup. Taking inspirations from other frameworks such as Django, SpringBoot and Laravel, flask-easy takes care of setting up your flask application with all the necessary dependencies, structure so that all you need to think of is churn out your precious features.

## Installation

    pip install flask-easy

## Getting Started
Once installed, run the scaffolding command and follow the prompt by selecting your desired setup
```
easy-admin scaffold <project-path>
```
OR
```
easy-admin scaffold .
```
When specified with a `.`, the project will be spawned in the current directory



# Features

## Routing
Flask easy is built on top of flask as it's name suggests so routing is basically the same with one caveat ``urls.py``
#### urls.py
When a project is generated, it is accompanied by a urls.py file.

```python
from flask_easy import route

routes = []
```
This is where you register all your blueprints.
```python
from flask_easy import route
from app.views import example # Note that example is a blueprint
from app.views import example_2

routes = [
    route(example),
    route(example_2, url_prefix="api/v1/example")
]
```
