import click

from nucleus.system.click import CustomCommand


# TODO: Need complete
# def cli_group(f):
#     def inner(*args, **kwargs):
#         pass
#         real_func =(f)
#         return real_func(*args, **kwargs)
#
#     return click.group('test', cls=CommandGroup)(f)


def cli_command(name=None, **attrs):
    def inner(f):
        return click.command(name, cls=CustomCommand, **attrs)(f)
    return inner
