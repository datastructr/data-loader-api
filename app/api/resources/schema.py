from flask_restful import Resource

from app.api import api
from app.api.controllers import schema


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


# Add resource endpoints here =================================================
api.add_resource(Schema, '/schema/<table_name>')
api.add_resource(SchemaList, '/schema')
