"""
model.py

Author: Joseph Maclean Arhin
"""

import os
import click
from jinja2 import Template

from .utils import add_to_init, convert_to_camelcase


def create_model(root_path, name, is_sql=True):
    """
    This function creates a model with the name specified. The model
    is created in the rootdir/models directory and its auto imported
    in the models __init__.py file.

    """
    name = name.lower()
    file_dir = os.path.join(root_path, "models")
    if not os.path.exists(file_dir):
        click.echo(click.style(f"cannot find models in {root_path}", fg="red"))
    file_name = f"{name}.py"
    model_name = convert_to_camelcase(name)

    template_string = get_template_string(is_sql)
    template = Template(template_string)
    data = template.render(model_name=model_name)
    file_path = os.path.join(file_dir, file_name)
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="UTF-8") as file:
            file.write(data)

        add_to_init(file_dir, name, model_name)
    else:
        click.echo(f"{name}.py exits")


def get_template_string(sql):
    """generate template string"""
    if sql:
        template_string = """from flask_easy import db, fields


class {{model_name}}(db.Model):
    pass

"""
    else:
        template_string = """import mongoengine as me


class {{model_name}}(me.Document):
    id = me.IntField(primary_key=True)

"""

    return template_string
