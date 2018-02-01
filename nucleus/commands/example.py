import click
from nucleus.system.click import CustomCommand


@click.group(cls=CustomCommand, help="Simple example of command [system]")
def example():
    print("EXAMPLE")
