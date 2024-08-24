import click

from demoapp.commands.create_database_command import create_db
from demoapp.commands.create_post_command import create_post


@click.group()
def cli() -> None:
    pass


cli.add_command(create_post)
cli.add_command(create_db)
