
import click
from cookiecutter.main import cookiecutter


@click.group()
def cli():
    pass


@cli.group()
def generate():
    pass


@cli.command("scaffold")
@click.argument("output_dir", required=False)
def scaffold(output_dir: str):
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
