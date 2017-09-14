#!/usr/bin/env python3

from dotenv import load_dotenv, find_dotenv
import os
from sqlalchemy import create_engine


load_dotenv(find_dotenv())

# Database Credentials
DB_CONNECTION = os.environ.get('DB_CONNECTION', 'sqlite')
DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_DATABASE = os.environ.get('DB_DATABASE', 'item_catalogue')

# Google OAuth credentials
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')

# Facebook OAuth credentials
FB_APP_ID = os.environ.get('FB_APP_ID')
FB_APP_SECRET = os.environ.get('FB_APP_SECRET')
FB_VERSION = os.environ.get('FB_VERSION', 'v2.10')

# App Config
APP_HOST = os.environ.get('APP_HOST', '0.0.0.0')
APP_PORT = int(os.environ.get('APP_PORT', 8000))
APP_SECRET_KEY = os.environ.get('APP_SECRET_KEY', 'super_secret_key')
# Username used in Database Seeds @see app/seeds.py
USER_NAME_FOR_DB_SEEDS = os.environ.get('USER_NAME_FOR_DB_SEEDS')
# Email Id used in Database Seeds @see app/seeds.py
USER_EMAIL_FOR_DB_SEEDS = os.environ.get('USER_EMAIL_FOR_DB_SEEDS')

engine = None
if DB_CONNECTION == 'sqlite':
    engine = create_engine('sqlite:///{}.db'.format(DB_DATABASE))
elif DB_CONNECTION == 'pgsql':
    engine = create_engine(
        'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
            DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE
        )
    )
elif DB_CONNECTION == 'mysql':
    engine = create_engine(
        'mysql+mysqldb://{}:{}@{}:{}/{}'.format(
            DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE
        )
    )
else:
    raise RuntimeError(
        'Unsupported database connection "{}" provided.'.format(
            DB_CONNECTION
        )
    )
