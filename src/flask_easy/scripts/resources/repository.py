"""
repository.py

Author: Joseph Maclean Arhin
"""
import os
import click
from jinja2 import Template

from .utils import convert_to_camelcase, remove_suffix, add_to_init


def create_repository(path, name, is_sql=True):
    """
    This method creates a repository in the rootdir/repositories
    directory with the name specified.
    """
    name = name.lower()
    file_dir = os.path.join(path, "repositories")
    if not os.path.exists(file_dir):
        click.echo(click.style(f"cannot find models in {path}", fg="red"))
    file_name = f"{name}.py"
    repo_name = convert_to_camelcase(name)
    model_name = remove_suffix(name, "repository")

    template_string = get_template_string(is_sql)
    template = Template(template_string)
    data = template.render(repo_name=repo_name, model_name=model_name.capitalize())
    file_path = os.path.join(file_dir, file_name)
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="UTF-8") as file:
            file.write(data)
        add_to_init(file_dir, f"{name}", f"{repo_name}")
    else:
        click.echo(f"{name}.py exists")


def get_template_string(is_sql):
    """
    Generate template string
    :param sql:
    :return:
    """
    if is_sql:
        template_string = """from flask_easy.repository.sql import Repository
from app.models import {{model_name}}


class {{repo_name}}(Repository):
    model = {{model_name}}

"""
    else:
        template_string = """from flask_easy.repository.mongo import Repository
from app.models import {{model_name}}


class {{repo_name}}(Repository):
    model = {{model_name}}

"""

    return template_string
