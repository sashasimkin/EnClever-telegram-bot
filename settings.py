import os
from mongoengine import register_connection

PROJECT_ROOT = os.path.dirname(__file__)


MONGO_DB_URI = os.getenv('MONGO_DB_URI', 'mongodb://localhost/testdb')


register_connection(
    'default',
    host=MONGO_DB_URI,
)
