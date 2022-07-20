"""
cli.py

Author: Joseph Maclean Arhin
"""
import click
from flask import Flask
from peewee_migrate import Router
from .resources import create_model, create_repository, create_view

MIGRATION_ERROR = ("migrations can only be run on sql databases",)


def init_cli(app: Flask, db_conn):  # pylint: disable=R0915
    """initialize all cli commands"""

    @click.group()
    def easy():
        """perform easy actions"""

    @easy.group()
    def generate():
        """perform scaffolding actions"""

    def get_db():
        config = app.config
        return config["DATABASE"].get("engine")

    @easy.command("db:seed")
    @click.argument("cycle", required=False, type=int)
    @click.option("--class_name", "-c")
    def seed(cycle: int, class_name: str):
        """
        seed database
        :param cycle:
        :param class_name:
        :return:
        """
        from flask_easy.factory import run_seeder  # pylint: disable=C0415

        count = cycle if cycle else 1
        click.echo("seeding...")
        run_seeder(count, class_name, app)
        click.echo(click.style("seeding complete!!!", fg="bright_green"))

    @easy.command("make:migration")
    @click.argument("name", required=False)
    def gen(name: str):
        """
        make migration
        :param name:
        :return:
        """
        if get_db() == "mongodb":
            click.echo(
                click.style(
                    MIGRATION_ERROR,
                    fg="bright_red",
                )
            )
        else:
            router = Router(db_conn.database)
            if not name:
                router.create(auto=True)
            else:
                router.create(name, auto=True)

    @easy.command("migrate")
    @click.argument("name", required=False)
    @click.option("--fake", "-f", "fake", is_flag=True)
    def migrate(name: str, fake: bool):
        if get_db() == "mongodb":
            click.echo(
                click.style(
                    MIGRATION_ERROR,
                    fg="bright_red",
                )
            )
        else:
            router = Router(db_conn.database)
            if not name:
                router.run(fake=fake)
            else:
                router.run(name, fake=fake)

    @easy.command("migrate:rollback")
    @click.argument("name", required=False)
    @click.option("--steps", "-s", "steps", type=int, default=1)
    def rollback(name: str, steps: int):
        if get_db() == "mongodb":
            click.echo(
                click.style(
                    MIGRATION_ERROR,
                    fg="bright_red",
                )
            )
        else:
            router = Router(db_conn.database)

            if not name:
                if steps > len(router.done):
                    click.echo(
                        click.style(
                            f"steps is greater than available number migrations({len(router.done)})",
                            fg="bright_red",
                        )
                    )
                    return
                if steps < 1:
                    click.echo(click.style("invalid number of steps", fg="bright_red"))
                    return

                for _ in range(steps):
                    last_migration = router.done[-1]
                    router.rollback(last_migration)
            else:
                router.rollback(name)

    @easy.command("migrate:list")
    def list_():
        if get_db() == "mongodb":
            click.echo(
                click.style(
                    MIGRATION_ERROR,
                    fg="bright_red",
                )
            )
        else:
            router = Router(db_conn.database)
            click.echo(
                click.style("Migrations done:", fg="bright_green", underline=True)
            )
            click.echo("\n".join(router.done))
            click.echo("")
            click.echo(click.style("Migrations to do:", underline=True))
            click.echo("\n".join(router.diff))

    @generate.command("model")
    @click.argument("name")
    @click.option("-r", "--repository", "repository", is_flag=True)
    def generate_model(name: str, repository):
        config = app.config
        if config:
            try:
                db_engine = get_db()
                if db_engine == "mongodb":
                    create_model(app.root_path, name, is_sql=False)
                    is_sql = False
                else:
                    create_model(app.root_path, name)
                    is_sql = True

                if repository:
                    create_repository(
                        app.root_path, f"{name}_repository", is_sql=is_sql
                    )

                click.echo(
                    click.style(
                        f"{name} model and repository created successfully",
                        fg="bright_green",
                    )
                )
            except AttributeError:
                click.echo(click.style("database engine not set", fg="red"))

    @generate.command("repository")
    @click.argument("name")
    def generate_repository(name: str):
        config = app.config
        if config:
            try:
                db_engine = get_db()
                if db_engine == "mongodb":
                    create_repository(
                        app.root_path,
                        f"{name}_repository",
                        is_sql=False,
                    )
                else:
                    create_repository(app.root_path, f"{name}_repository")

                click.echo(
                    click.style(
                        f"{name} repository created successfully", fg="bright_green"
                    )
                )
            except AttributeError:
                click.echo(click.style("database engine not set", fg="red"))

    @generate.command("view")
    @click.argument("name", required=False)
    def generate_view(name: str):
        create_view(app, name)
        click.echo(click.style(f"{name}_view generated successfully", fg="green"))

    app.cli.add_command(easy)
    app.cli.add_command(generate)
