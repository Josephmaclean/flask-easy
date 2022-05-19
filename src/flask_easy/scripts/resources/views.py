import os
import pathlib
import click
from jinja2 import Template
from .utils import convert_to_camelcase, add_to_init


def create_view(app, name):
    """
    This function creates a view with the name specified.
    This view is created in the rootdir/views
    directory and its auto imported in the __init__.py file

    """
    name = name.lower()
    file_dir = os.path.join(app.root_path, "views")
    if not os.path.exists(file_dir):
        pathlib.Path(file_dir).mkdir(parents=True, exist_ok=True)
    file_name = f"{name}_view.py"

    template_details = {
        "route_name": name,
    }
    template_string = """from flask_easy import ResponseEntity, Blueprint
    
{{route_name}} = Blueprint("{{route_name}}", __name__)


@{{route_name}}.get("/{{route_name}}/hello")
def hello_{{route_name}}():
    return ResponseEntity.ok({"greeting": "hello"})

"""

    template = Template(template_string)
    data = template.render(**template_details)
    file = os.path.join(file_dir, file_name)
    if not os.path.exists(file):
        with open(file, "w") as w:
            w.write(data)
        click.echo(f"{name} generated successfully")
        add_to_init(file_dir, f"{name}_view", name)
