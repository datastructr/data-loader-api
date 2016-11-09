import os

from flask import Flask

from app.config import ProductionConfig, DevelopmentConfig
from app.extensions import (
    db,
    migrate,
)
from app.api import api_blueprint


if os.getenv("FLASK_ENV") == 'prod':
    DefaultConfig = ProductionConfig
else:
    DefaultConfig = DevelopmentConfig

def create_app(config_object=DefaultConfig):
    '''A flask application factory

    :param config_object: The configuration object to use.
    :returns: flask.Flask object
    '''
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    """Call the method 'init_app' to register the extensions in the flask.Flask
    object passed as parameter.

    :app: flask.Flask object
    :returns: None

    """
    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    """Register all blueprints.

    :app: flask.Flask object
    :returns: None

    """
    app.register_blueprint(api_blueprint)
