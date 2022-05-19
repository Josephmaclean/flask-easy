import click
from flask import Flask
from peewee_migrate import Router
from .resources import create_model, create_repository, create_view


def init_cli(app: Flask, db):
    @click.group()
    def easy():
        """perform easy actions"""
        pass

    @easy.group()
    def generate():
        pass

    @easy.command("make:migration")
    @click.argument("name", required=False)
    def gen(name: str):
        """
        eyc
        :param name:
        :return:
        """
        router = Router(db.database)
        if not name:
            router.create(auto=True)
        else:
            router.create(name, auto=True)

    @easy.command("migrate")
    @click.argument("name", required=False)
    @click.option("--fake", "-f", "fake", is_flag=True)
    def migrate(name: str, fake: str):
        router = Router(db.database)
        if not name:
            router.run(fake=fake)
        else:
            router.run(name, fake=fake)

    @easy.command("migrate:rollback")
    @click.argument("name", required=False)
    @click.option("--steps", "-s", "steps", type=int, default=1)
    def rollback(name: str, steps: int):
        router = Router(db.database)

        if not name:
            if steps > len(router.done):
                click.echo(click.style(f"steps is greater than available number migrations({len(router.done)})",
                                       fg="bright_red"))
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
    def list():
        router = Router(db.database)
        click.echo(click.style('Migrations done:', fg="bright_green", underline=True))
        click.echo('\n'.join(router.done))
        click.echo('')
        click.echo(click.style('Migrations to do:', underline=True))
        click.echo('\n'.join(router.diff))

    @generate.command("model")
    @click.argument("name")
    def generate_model(name: str):
        config = app.config
        if config:
            try:
                db_engine = config["DB_ENGINE"]
                if db_engine == "mongodb":
                    create_model(app.root_path, name, is_sql=False)
                    create_repository(
                        app.root_path, f"{name}_repository", is_sql=False
                    )
                else:
                    create_model(app.root_path, name)
                    create_repository(
                        app.root_path, f"{name}_repository"
                    )

                click.echo(
                    click.style(
                        f"{name} model and repository created successfully",
                        fg="bright_green",
                    )
                )
            except AttributeError:
                click.echo(click.style("DB_ENGINE not set", fg="red"))

    @generate.command("repository")
    @click.argument("name", required=False)
    @click.option("-m", "--model", "model")
    def generate_repository(name: str, model: str):
        config = app.config
        if config:
            try:
                db_engine = config["DB_ENGINE"]
                if db_engine == "mongodb":
                    create_repository(
                        app.root_path,
                        f"{name}_repository",
                        is_sql=False,
                    )
                else:
                    create_repository(
                        app.root_path, f"{name}_repository"
                    )

                click.echo(
                    click.style(
                        f"{name} repository created successfully", fg="bright_green"
                    )
                )
            except AttributeError:
                click.echo(click.style("DB_ENGINE not set", fg="red"))

    @generate.command("view")
    @click.argument("name", required=False)
    def generate_view(name: str):
        create_view(app, name)

    app.cli.add_command(easy)
    app.cli.add_command(generate)
