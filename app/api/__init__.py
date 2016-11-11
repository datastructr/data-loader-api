from flask import Blueprint
from flask_restful import Api


api_blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_blueprint)

# Add Resources ===============================================================
#       must import resources last to instantiate the add_resources after
#       blueprint creation
from .resources import (
    schema,
    upload,
)
