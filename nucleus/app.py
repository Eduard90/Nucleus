import sys
from sanic import Sanic
from sanic_jwt import initialize
import importlib
from nucleus.kafka import ConsumerMessage

try:
    import aiokafka

    kafka_module = aiokafka
except ImportError:
    kafka_module = None

from nucleus.kafka.exceptions import KafkaTopicHandlerNotFound
from nucleus.exceptions import MiddlewareImportError
from nucleus.urls import WSRoute, HTTPRoute
from nucleus.utils.modules import get_function_from_string


class App(Sanic):
    __kafka_enabled = False
    __kafka_producer = None
    __kafka_consumer = None
    __kafka_topics_handlers = {}

    payload = {}  # Write

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_kafka_producer(self, producer):
        self.__kafka_producer = producer

    @property
    def kafka_producer(self):
        return self.__kafka_producer

    def set_kafka_consumer(self, consumer):
        self.__kafka_consumer = consumer

    @property
    def kafka_consumer(self):
        return self.__kafka_consumer

    def get_kafka_topic_handler(self, topic: str):
        return self.__kafka_topics_handlers[topic]

    def set_kafka_topic_handler(self, topic: str, handler):
        self.__kafka_topics_handlers[topic] = handler

    @property
    def kafka_enabled(self):
        return self.__kafka_enabled

    def import_project_urls(self):
        try:
            urls_module = importlib.import_module('urls')
            route_list = getattr(urls_module, 'urls')
            for route in route_list:
                if isinstance(route, HTTPRoute):  # Add http route
                    self.add_route(route.handler, route.uri, route.methods, route.host, route.strict_slashes,
                                   route.version, route.name)
                elif isinstance(route, WSRoute):  # Add websocket route
                    self.add_websocket_route(route.handler, route.uri, route.host, route.strict_slashes, route.name)

        except (ModuleNotFoundError, AttributeError) as e:
            print(e)

    def import_project_middlewares(self):
        last_middleware = ''
        try:
            for middleware in app.config.MIDDLEWARES:
                last_middleware = middleware
                func = get_function_from_string(middleware)
                self.register_middleware(func)
        except (ModuleNotFoundError, AttributeError) as e:
            raise MiddlewareImportError(last_middleware)

    def init_project_listeners(self):
        try:
            func = get_function_from_string('listeners.before_server_start')
            self.listener('before_server_start')(func)
        except (ModuleNotFoundError, AttributeError):
            pass

        try:
            func = get_function_from_string('listeners.before_server_stop')
            self.listener('before_server_stop')(func)
        except (ModuleNotFoundError, AttributeError):
            pass

    def init_auth(self):
        if self.config.AUTH_INIT_FUNC is None:
            return

        func = get_function_from_string(self.config.AUTH_INIT_FUNC)
        initialize(self, func)

    def run(self, *args, **kwargs):
        if self.config.KAFKA_BOOTSTRAP_SERVER and kafka_module is None:
            print("Warning! KAFKA_BOOTSTRAP_SERVER is set but aiokafka not installed!")

        if kafka_module is None:
            self.__kafka_enabled = False
        else:
            self.__kafka_enabled = False if self.config.KAFKA_BOOTSTRAP_SERVER is None else True

        app.import_project_urls()
        app.import_project_middlewares()
        app.import_project_middlewares()
        app.init_project_listeners()
        app.init_auth()
        # TODO: Need replace to @listener
        app.add_task(kafka_init(self))

        if self.__kafka_enabled:
            @self.listener('before_server_stop')
            async def stop_kafka(app, loop):
                if self.__kafka_consumer:
                    await self.__kafka_consumer.stop()
                if self.__kafka_producer:
                    await self.__kafka_producer.stop()

        super().run(*args, **kwargs)


async def kafka_init(app):
    if not app.kafka_enabled:
        return

    producer = aiokafka.AIOKafkaProducer(loop=app.loop, bootstrap_servers=app.config.KAFKA_BOOTSTRAP_SERVER)
    consumer = None
    if app.config.KAFKA_CONSUMER_TOPICS:
        for topic in app.config.KAFKA_CONSUMER_TOPICS:
            handlers_module = importlib.import_module('kafka_handlers')
            try:
                topic_handler = getattr(handlers_module, 'handler_{}'.format(topic))
                app.set_kafka_topic_handler(topic, topic_handler)
            except AttributeError:
                raise KafkaTopicHandlerNotFound(topic)

        consumer = aiokafka.AIOKafkaConsumer(*app.config.KAFKA_CONSUMER_TOPICS, loop=app.loop,
                                             bootstrap_servers=app.config.KAFKA_BOOTSTRAP_SERVER)

    try:
        await producer.start()
        app.set_kafka_producer(producer)
        if consumer:
            await consumer.start()
            app.set_kafka_consumer(consumer)
    except ConnectionError:
        print("Can't connect to Kafka server.")
        sys.exit(1)

    if app.kafka_consumer:
        async for msg in app.kafka_consumer:
            message = ConsumerMessage(app, msg)
            await app.get_kafka_topic_handler(msg.topic)(message)


app = App()
