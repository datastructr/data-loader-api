from flask_restful import Resource, request

from app.api import api
from app.api.controllers import schema
from app.utils import abort_bad_upload_json

# Import test JSON data
from app.data import (
    test_table_json,
    test_multiple_json,
)


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

        if 'multiple' in json_data:
            for table in test_multiple_json['multiple']:
                if 'table' in table and 'data' in table:
                    response = schema.post_table(table)
                else:
                    return abort_bad_upload_json()
        else:
            if 'table' in json_data and 'data' in json_data:
                response = schema.post_table(test_table_json)
            else:
                return abort_bad_upload_json()

        return response

# Add resource endpoints here =================================================
api.add_resource(Schema, '/schema/<table_name>')
api.add_resource(SchemaList, '/schema')
api.add_resource(Upload, '/upload')
