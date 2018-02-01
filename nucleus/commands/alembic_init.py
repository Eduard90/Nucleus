import click


@click.command(help="Init alembic migrations")
def alembic_init():
    """
    @deprecated
    :return:
    """
    pass
    # import os
    # import shutil
    # from nucleus.conf import settings
    #
    # from nucleus import nucleus_package_path
    # src_alembic_ini_path = os.path.join(nucleus_package_path, 'alembic.ini')
    # src_alembic_dir_path = os.path.join(nucleus_package_path, 'alembic')
    # dest_alembic_dir_path = os.path.join(settings['BASE_DIR'], 'alembic')
    #
    # shutil.copy(src_alembic_ini_path, settings['BASE_DIR'])
    # shutil.copytree(src_alembic_dir_path, dest_alembic_dir_path)
