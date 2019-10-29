import os


class Config:
    ERROR_404_HELP = False

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    ROOT_URL = ''

    DATABASE_HOST = ''
    DATABASE_USER = ''
    DATABASE_PASSWORD = ''
    DATABASE_PORT = '5432'
    DATABASE_NAME = 'db_taphee'
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}'


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestConfig(Config):
    DEBUG = True
    TESTING = True
