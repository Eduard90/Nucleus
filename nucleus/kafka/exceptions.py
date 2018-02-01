class KafkaError(Exception):
    pass


class KafkaTopicHandlerNotFound(KafkaError):
    def __init__(self, topic):
        super().__init__("Can't find handler for topic '{}'".format(topic))