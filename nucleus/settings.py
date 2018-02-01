import os

AUTH_INIT_FUNC = None
MIDDLEWARES = []

# PostgreSQL settings
USE_DB = True
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DATABASE = os.getenv('DB_DATABASE')
DB_PORT = os.getenv('DB_PORT', 5432)

# Web settings
WEB_PORT = os.getenv('WEB_PORT', 8000)

# Kafka settings
KAFKA_BOOTSTRAP_SERVER = os.getenv('KAFKA_BOOTSTRAP_SERVER', None)
KAFKA_CONSUMER_TOPICS = []

