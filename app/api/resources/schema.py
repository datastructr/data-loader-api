import json
from flask_restful import Resource, request

from app.api import api
from app.api.controllers import schema

# Import test JSON data
from app.data import test_json


class Schema(Resource):
    """Schema Class is the Resource for a single table schema
    in a database

    :extends Resource
    :returns: a JSON response
    """
    def get(self, table_name):
        response = schema.get_single_table(table_name)
        return response


class SchemaList(Resource):
    """SchemaList Class is the Resource for fetching all table schemas
    in a database

    :extends Resource
    :returns: a JSON response
    """
    def get(self):
        response = schema.get_tables()
        return response


class Upload(Resource):
    """Upload Class is the Resource for uploading a data to a single table

    :extends Resource
    :returns: a JSON response
    """
    def post(self):
        json_data = request.get_json(force=True)

        if 'table' in json_data and 'data' in json_data:
            response = schema.post_table(test_json)
        else:
            return {'message': 'You must specify a table with data to upload'}

        return response

# Add resource endpoints here =================================================
api.add_resource(Schema, '/schema/<table_name>')
api.add_resource(SchemaList, '/schema')
api.add_resource(Upload, '/upload')
