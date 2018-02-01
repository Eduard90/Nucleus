class Route:
    __handler = None
    __uri = ''
    __host = None
    __strict_slashes = None
    __version = None
    __name = None

    def __init__(self, handler, uri, host=None, strict_slashes=None, version=None, name=None):
        self.__handler = handler
        self.__uri = uri
        self.__host = host
        self.__strict_slashes = strict_slashes
        self.__version = version
        self.__name = name

    @property
    def handler(self):
        return self.__handler

    @property
    def uri(self):
        return self.__uri

    @property
    def host(self):
        return self.__host

    @property
    def strict_slashes(self):
        return self.__strict_slashes

    @property
    def version(self):
        return self.__version

    @property
    def name(self):
        return self.__name


class WSRoute(Route):
    pass


class HTTPRoute(Route):
    __methods = ('GET',)

    def __init__(self, handler, uri, methods=None, host=None, strict_slashes=None, version=None, name=None):
        super().__init__(handler, uri, host, strict_slashes, version, name)
        if methods is not None:
            self.__methods = methods

    @property
    def methods(self):
        return self.__methods
