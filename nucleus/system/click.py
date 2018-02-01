import os
import asyncio
from click import Group, Command
from nucleus.system.dotenv import load_dotenv
import importlib
from nucleus.utils import connect_to_pg


class AutoImportGroup(Group):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        commands_path = 'commands'
        if os.path.isdir('{}'.format(commands_path.replace('.', '/'))):
            tree = os.listdir('{}'.format(commands_path.replace('.', '/')))
            for filename in tree:
                if '__' in filename:
                    continue
                package_name = filename.replace('.py', '')
                module_name = "{}.{}".format(commands_path, package_name)
                module = importlib.import_module(module_name)
                func = getattr(module, package_name)
                self.add_command(func)

                # print(filename)
        # local_commands = importlib.import_module('commands')
        # print(local_commands)
        # for command in dir(local_commands):
        #     print(command)

        # commands_path = 'commands'
        # print(filepath)
        #
        # try:
        #     commands_path_idx = filepath.index(commands_path)
        #     short_path = filepath[commands_path_idx + len(commands_path) + 1:]
        #     path_parts = short_path.split('/')
        #     subpath = path_parts[0] if len(path_parts) > 1 else ''
        #     fullpath = [commands_path, subpath]
        #     path_to_subcommands = os.path.join(*fullpath)
        #     tree = os.listdir('{}'.format(path_to_subcommands))
        #     print(path_to_subcommands)
        #     for filename in tree:
        #         if '__' in filename:
        #             continue
        #         package_name = filename.replace('.py', '')
        #         parent_package = path_to_subcommands.replace('/', '.')
        #         parent_package = parent_package.strip('.')
        #         module_name = "{}.{}".format(parent_package, package_name)
        #         module = importlib.import_module(module_name)
        #         func = getattr(module, package_name)
        #         self.add_command(func)
        # except ValueError as e:
        #     raise e
        #     pass


class CommandGroup(AutoImportGroup):
    def __init__(self, *args, **kwargs):
        load_dotenv('.env')
        super().__init__(*args, **kwargs)

    def get_help(self, ctx):
        print("Welcome to {}.".format(os.getenv('PROJECT_NAME', "PLEASE_FILL_PROJECT_NAME")))
        return super().get_help(ctx)


class CustomCommand(Command):
    loop = None

    def __init__(self, *args, **kwargs):
        load_dotenv('.env')
        self.loop = asyncio.get_event_loop()

        super().__init__(*args, **kwargs)

    def invoke(self, ctx):
        from nucleus.conf import settings

        if asyncio.iscoroutinefunction(self.callback):
            self.loop.run_until_complete(
                connect_to_pg(settings.DB_HOST, settings.DB_PORT, settings.DB_USER, settings.DB_PASSWORD,
                              settings.DB_DATABASE, self.loop))
            self.loop.run_until_complete(self.callback(**ctx.params))
        else:
            super().invoke(ctx)
