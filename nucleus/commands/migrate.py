import click


@click.command(help="Apply migrations [system]")
def migrate():
    import os
    from nucleus.conf import settings
    from alembic.config import Config
    from alembic.command import upgrade

    alembic_ini_path = os.path.join(settings['BASE_DIR'], 'alembic.ini')
    alembic_cfg = Config(alembic_ini_path)
    upgrade(alembic_cfg, "head")
