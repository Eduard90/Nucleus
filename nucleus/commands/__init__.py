import click
from nucleus.system.click import CommandGroup
from nucleus.commands.example import example
from nucleus.commands.makemigrations import makemigrations
from nucleus.commands.migrate import migrate
from nucleus.commands.alembic_init import alembic_init
from nucleus.commands.run import run
from nucleus.commands.test import test


@click.group(cls=CommandGroup)
def cli():
    pass


cli.add_command(example)
cli.add_command(alembic_init)
cli.add_command(makemigrations)
cli.add_command(migrate)
cli.add_command(run)
cli.add_command(test)
