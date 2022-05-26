"""
easy_scripts.py

Author: Joseph Maclean Arhin
"""

import click
from cookiecutter.main import cookiecutter


@click.group()
def cli():
    """
    base cli command
    :return: None
    """


@cli.command("scaffold")
@click.argument("output_dir", required=False)
def scaffold(output_dir: str):
    """
    Spawn a new project
    :param output_dir:
    :return:
    """
    if output_dir is None:
        val = click.prompt("Project name")
        extra_context = {"_project_name": val}
    else:
        extra_context = {"_project_name": "My Awesome App", "_remove_parent": True}
    cookiecutter(
        "https://github.com/Josephmaclean/easy-scaffold.git",
        output_dir=output_dir,
        extra_context=extra_context,
    )


if __name__ == "__main__":
    cli()
