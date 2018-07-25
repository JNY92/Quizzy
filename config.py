import os
import logging

# bd config
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True

pg_connection_string = 'postgresql+psycopg2://{username}:{password}@{hostname}:{port}/{database}'

SQLALCHEMY_DATABASE_URI = pg_connection_string.format(
    username='vfquiz',
    password='vfquiz',
    hostname='dchaos.cfpz9wwo4rqd.us-east-1.rds.amazonaws.com',
    port='5432',
    database='vfquiz'
)

SQLALCHEMY_POOL_SIZE ='10'
SQLALCHEMY_POOL_TIMEOUT = '2'

# log config
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
