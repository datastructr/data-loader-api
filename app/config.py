import os


class BaseConfig(object):
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

    ERROR_404_HELP = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://'
    SECRET_KEY = '1d94e52c-1c89-4515-b87a-f48cf3cb7f0b'


class ProductionConfig(BaseConfig):
    """Production configuration."""
    ENV = 'production'
    DEBUG = False
    # DB URL variable set in env
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '')


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    ENV = 'development'
    DEBUG = True
    DB_NAME = 'bids_02'
    DB_PATH = os.path.join(BaseConfig.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost/bids_02'


class TestingConfig(BaseConfig):
    """Test configuration."""
    ENV = 'testing'
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://'
