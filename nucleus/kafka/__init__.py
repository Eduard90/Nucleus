class ConsumerMessage:
    __app = None
    __message = None

    def __init__(self, app, message):
        self.__app = app
        self.__message = message

    @property
    def app(self):
        return self.__app

    @property
    def message(self):
        return self.__message

    def __repr__(self):
        return "<ConsumerMessage app='{}' consumer_record='{}'>".format(self.app, self.message)
