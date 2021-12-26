"""Resource generators"""

import os
import pathlib
import click
from flask import Flask
from flask.cli import AppGroup
from jinja2 import Template


def init_generators(app: Flask):
    """Cli command to initialize resource generators"""
    gen_cli = AppGroup("generate")

    @gen_cli.command("repository")
    @click.argument("name")
    def generate_repository(name: str):
        """Command to generate repository"""
        create_repository(app, name)

    @gen_cli.command("model")
    @click.argument("name")
    @click.option("--repository", "-r", "repo", is_flag=True)
    @click.option("--view", "-c", "view", is_flag=True)
    @click.option("--all", "-a", "all", is_flag=True)
    def generate_model(name: str, repo: str, view: str, all: str):
        """Command to generate models"""
        create_model(app, name)

        if all:
            create_repository(app, f"{name}_repository")
            create_view(app, f"{name}_view")
        else:
            if repo:
                create_repository(app, f"{name}_repository")

            if view:
                create_view(app, f"{name}_view")

    @gen_cli.command("view")
    @click.argument("name")
    def generate_view(name: str):
        """Command to generate views"""
        create_view(app, name)

    app.cli.add_command(gen_cli)


def add_to_init(dir_path, file_name, class_name):
    with open(os.path.join(dir_path, "__init__.py"), "a") as w:
        w.write(f"from .{file_name} import {class_name}\n")


def convert_to_camelcase(string: str):
    """
    Algorithm to convert snake_case to CamelCase
    """
    s = list(string)

    if s[-1] == "_":
        s[-1] = ""

    for i in range(len(s), 0, -1):
        if s[i - 1] == "_":
            s[i - 1] = ""
            s[i] = s[i].upper()
    s[0] = s[0].upper()

    return "".join(s)


def remove_suffix(string: str, suffix):
    """
    Remove suffix from string if its last characters are equal to
    the suffix passed.
    """
    suffix_length = len(suffix) - 1
    string_length = len(string) - 1
    cut_off_index = string_length - suffix_length

    if string_length <= suffix_length:
        final_string = string

    elif string[cut_off_index:] == suffix:
        final_string = string[:cut_off_index]

    else:
        final_string = string

    if final_string[-1] == "_":
        final_string = final_string[:-1]

    return final_string.lower()


def create_repository(app, name):
    """
    This method creates a repository in the rootdir/repositories
    directory with the name specified.
    """
    name = name.lower()
    file_dir = os.path.join(app.root_path, "repositories")
    if not os.path.exists(file_dir):
        pathlib.Path(file_dir).mkdir(parents=True, exist_ok=True)
    file_name = f"{name}.py"
    repo_name = convert_to_camelcase(name)
    model_name = remove_suffix(name, "repository")

    template_string = """from core.repository import SqlBaseRepository
from app.models import {{model_name}}


class {{repo_name}}(SqlBaseRepository):
    model = {{model_name}}

"""
    template = Template(template_string)
    data = template.render(repo_name=repo_name, model_name=model_name.capitalize())
    file = os.path.join(file_dir, file_name)
    if not os.path.exists(file):
        with open(file, "w") as w:
            w.write(data)
        add_to_init(file_dir, f"{name}", f"{repo_name}")
    else:
        click.echo(f"{name}.py exists")

    click.echo(f"{name.capitalize()} created successfully")


def create_model(app, name):
    """
    This function creates a model with the name specified. The model
    is created in the rootdir/models directory and its autoimported
    in the models __init__.py file.

    """
    name = name.lower()
    file_dir = os.path.join(app.root_path, "models")
    if not os.path.exists(file_dir):
        pathlib.Path(file_dir).mkdir(parents=True, exist_ok=True)
    file_name = f"{name}.py"
    model_name = convert_to_camelcase(name)

    template_string = """from core.extensions import db
from dataclasses import dataclass


@dataclass
class {{model_name}}(db.Model):
    id: int

    id = db.Column(db.Integer, primary_key=True)

"""
    template = Template(template_string)
    data = template.render(model_name=model_name)
    file = os.path.join(file_dir, file_name)
    if not os.path.exists(file):
        with open(file, "w") as w:
            w.write(data)

        add_to_init(file_dir, name, model_name)
    else:
        click.echo(f"{name}.py exits")


def create_view(app, name):
    """
    This function creates a view with the name specified.
    This view is created in the rootdir/views
    directory and its autoimported in the __init__.py file

    """
    name = name.lower()
    file_dir = os.path.join(app.root_path, "views")
    root_dir_name = os.path.basename(app.root_path)
    if not os.path.exists(file_dir):
        pathlib.Path(file_dir).mkdir(parents=True, exist_ok=True)
    file_name = f"{name}.py"
    class_name = convert_to_camelcase(name)
    repository_file_name = f"{name}_repository"
    repository_class_name = f"{class_name}"

    template_details = {
        "repository_file_name": repository_file_name,
        "repository_class_name": repository_class_name,
        "root_dir_name": root_dir_name,
        "class_name": class_name,
    }
    template_string = """from core.views import EasyView


class {{class_name}}(EasyView):
    def index(self):
        pass

    def create(self, data):
        pass

    def show(self, item_id):
        pass

    def update(self, item_id, data):
        pass

    def delete(self, item_id):
        pass

"""

    template = Template(template_string)
    data = template.render(**template_details)
    file = os.path.join(file_dir, file_name)
    if not os.path.exists(file):
        with open(file, "w") as w:
            w.write(data)
        click.echo(f"{name} generated successfully")
        add_to_init(file_dir, name, class_name)
