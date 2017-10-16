import os
from mongoengine import register_connection

PROJECT_ROOT = os.path.dirname(__file__)

BOT_TOKEN_FILENAME = 'tokens/token'
with open(os.path.join(PROJECT_ROOT, BOT_TOKEN_FILENAME), 'r') as f:
    BOT_TOKEN = f.read().replace("\n", "")


MONGO_DB_URI = os.getenv('MONGO_DB_URI', 'mongodb://localhost/testdb')


register_connection(
    'default',
    host=MONGO_DB_URI,
)
