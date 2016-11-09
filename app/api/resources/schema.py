from flask_restful import Resource, request

from app.api import api
from app.api.controllers import schema


# A single table schema
# describes the schema for a single table the api is connected to
class Schema(Resource):
    def get(self, table_name):
        response = schema.getSingleTable(table_name)
        if response[0] == 404:
            return 404
        else:
            return response


# Schema List
# describes the schema that the api is connected to
class SchemaList(Resource):
    def get(self):
        response = schema.getTables()
        if response[0] == 404:
            return 404
        else:
            return response

    # TODO in progress working on posting/parsing a json with specific fields to be uploaded to
    #       a valid table in the schema connected to
    def post(self):
        json_data = request.get_json(force=True)

        try:
            response = schema.postTables(json_data)
        except ValueError:
            return 'That was not a valid JSON Object to POST', 404

        return 'Cheers! Data uploaded.', 201

api.add_resource(Schema, '/schema/<table_name>')
api.add_resource(SchemaList, '/schema')
