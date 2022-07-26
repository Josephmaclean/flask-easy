"""
easy_scripts.py

Author: Joseph Maclean Arhin
"""

import os
import click
from copier import run_auto


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
    out_path = os.path.join(os.getcwd(), output_dir)
    if output_dir == ".":
        extra_context = {"default_project_name": os.path.split(os.getcwd())[1]}
    else:
        project_name = "_".join(output_dir.split(" "))
        extra_context = {"default_project_name": project_name}
        out_path = os.path.join(os.getcwd(), project_name)

    # copier.main.c
    run_auto("gh:josephmaclean/easy-scaffold-copier", out_path, data=extra_context)


if __name__ == "__main__":
    cli()
