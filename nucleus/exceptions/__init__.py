class AppRuntimeException(Exception):
    pass


class MiddlewareImportError(AppRuntimeException):
    def __init__(self, middleware: str):
        super().__init__("Middleware '{}' can't import. Please check.".format(middleware))