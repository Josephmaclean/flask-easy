"""
views.py

Author: Joseph Maclean Arhin
"""
import os
import pathlib
from jinja2 import Template
from .utils import add_to_init


def create_view(app, name):
    """
    This function creates a view with the name specified.
    This view is created in the rootdir/views
    directory and its auto imported in the __init__.py file

    """
    name = name.lower()
    root_path = app.root_path
    file_dir = os.path.join(root_path, "views")
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
    file_path = os.path.join(file_dir, file_name)
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="UTF-8") as file:
            file.write(data)
        add_to_init(file_dir, f"{name}_view", name)
    add_to_urls(root_path, name)


def add_to_urls(path, route_name):
    """
    import view in urls.py
    :param path:
    :param route_name:
    :return:
    """
    file_path = os.path.join(path, "urls.py")
    import_index = 0
    with open(file_path, encoding="UTF-8") as file:
        file_data = file.readlines()

        for i, j in enumerate(file_data):
            if j in ("\n", ""):
                import_index = i
                break
        imp = """from app.views import {{route_name}} \n\n
"""
    file_data[import_index] = Template(imp).render(route_name=route_name)

    with open(file_path, "w", encoding="UTF-8") as file:
        file.writelines(file_data)
