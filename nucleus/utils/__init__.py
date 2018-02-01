import importlib


async def connect_to_pg(host, port, user, password, database, loop):
    from nucleus.models import db
    await db.create_pool(host=host, port=port, user=user, password=password, database=database, loop=loop)


def load_all_models(local_vars=None, models_module_name='models'):
    from nucleus.models import db

    if local_vars is None:
        local_vars = {}
    models_module = importlib.import_module(models_module_name)
    for model_name in dir(models_module):
        cls = getattr(importlib.import_module(models_module_name), model_name)
        if isinstance(cls, type):
            if issubclass(cls, db.Model):
                local_vars[model_name] = cls


def run_web_application(settings):
    from nucleus.app import app
    from nucleus.models import db

    app.config.update(settings)

    if settings.USE_DB:  # Configure database
        db.init_app(app)

    app.run(host='0.0.0.0', port=settings.WEB_PORT)
