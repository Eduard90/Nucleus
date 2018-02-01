import click
import importlib


class Settings:
    __storage = {}

    def __init__(self):
        from nucleus import settings as nucleus_settings
        for var in dir(nucleus_settings):
            if var.startswith('__') or not var.isupper():
                continue
            var_val = getattr(nucleus_settings, var)
            setattr(self, var, var_val)

        project_settings_module = "settings"  # TODO: Need move to NUCLEUS_SETTINGS_MODULE env var
        try:
            settings_module = importlib.import_module(project_settings_module)
            for var in dir(settings_module):
                if var.startswith('__') or not var.isupper():
                    continue
                var_val = getattr(settings_module, var)
                setattr(self, var, var_val)
        except ModuleNotFoundError:
            click.echo(click.style("Please create 'settings.py' file for your project.", fg='red'))

    def __setattr__(self, key, value):
        self.__storage[key] = value

    def __getattr__(self, key):
        try:
            return self.__dict__[key]
        except KeyError:
            return self.__storage[key]

    def __iter__(self):
        for key, val in self.__storage.items():
            yield key, val

    def __getitem__(self, item):
        return self.__storage[item]


settings = Settings()
