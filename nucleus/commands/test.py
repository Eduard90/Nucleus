import click
from nucleus.system.click import CustomCommand


@click.command(cls=CustomCommand, help="Run tests [system]")
def test():
    import asyncio
    import os
    import pytest as module_pytest
    from alembic.config import Config
    from alembic.command import upgrade
    from nucleus.conf import settings
    from nucleus.models import db

    tests_dir = 'tests'
    full_path_tests = os.path.join(settings.BASE_DIR, tests_dir)
    if not os.path.isdir(full_path_tests):
        click.echo(click.style("Can't find tests directory in your project", fg='red'))
        return

    loop = asyncio.get_event_loop()

    async def connect_to_pg(future, loop):
        database = "test_{}".format(settings.DB_DATABASE)
        settings.DB_DATABASE = database
        pg_connect = await db.create_pool(host=settings.DB_HOST, port=settings.DB_PORT, user=settings.DB_USER,
                                          password=settings.DB_PASSWORD, loop=loop)
        await pg_connect.execute("DROP DATABASE IF EXISTS {}".format(settings.DB_DATABASE))
        await pg_connect.execute("CREATE DATABASE {}".format(settings.DB_DATABASE))
        alembic_ini_path = os.path.join(settings.BASE_DIR, 'alembic.ini')
        alembic_cfg = Config(alembic_ini_path)
        upgrade(alembic_cfg, "head")
        await pg_connect.close()
        pg_connect = await db.create_pool(host=settings.DB_HOST, port=settings.DB_PORT, user=settings.DB_USER,
                                          password=settings.DB_PASSWORD, database=settings.DB_DATABASE, loop=loop)
        future.set_result(pg_connect)

    async def disconnect_from_pg(pg_connect):
        await pg_connect.close()

    future = asyncio.Future()
    loop.run_until_complete(connect_to_pg(future, loop))
    connect = future.result()

    module_pytest.main([full_path_tests])

    loop.run_until_complete(disconnect_from_pg(connect))

