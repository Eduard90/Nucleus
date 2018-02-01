import importlib


def get_function_from_string(module_str: str):
    """
    Function get module string (ex. middlewares.my_middleware) and get function (my_middleware) and return function.
    :param module_str: Module string in your project (ex. middlewars.my_middleware)
    :return:
    """
    parent_module = '.'.join(module_str.split('.')[:-1])
    func_name = module_str.split('.')[-1]
    module = importlib.import_module(parent_module)
    func = getattr(module, func_name)
    return func
