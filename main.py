# System Imports
from os import getenv

# Third party imports
from flask import Flask
from flask_restplus import Api
from flask_migrate import Migrate

# Local ImportS
from config import config
from api import api_blueprint
from api.models.database import db


config_name = getenv('FLASK_ENV', default='production')
api = Api(api_blueprint, doc=False)

def initialize_blueprint(application):
    application.register_blueprint(api_blueprint)

migrate =Migrate()


def create_app(config=config.get(config_name)):
    """Return app object given config object."""
    app = Flask(__name__)
    app.config.from_object(config)
    initialize_blueprint(app)
    app.url_map.strict_slashes = False

    # initialize database
    db.init_app(app)
    # initialize migration app
    migrate.init_app(app,db)

    # import all models
    from api.models import usermodel

    # import views
    import api.views
    

    return app
