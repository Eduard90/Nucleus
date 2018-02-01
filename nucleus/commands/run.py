import click


@click.command(help="Run application [system]")
def run():
    from nucleus.utils import run_web_application
    from nucleus.conf.settings import settings

    run_web_application(settings)
