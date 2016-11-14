from flask_restful import Resource, request

from app.api import api
from app.api.controllers import upload
from app.helpers import api_response

# Import test JSON data
#       Create data module under /api module and create some test data
from app.data.bulk_upload import (
    test_table_json,
    test_multiple_json,
)


class Upload(Resource):
    """Upload Class is the Resource for uploading a data to a single table

    :extends Resource
    :returns: a JSON response
    """

    @api_response
    def post(self):
        json_data = request.get_json(force=True)

        response = []
        if 'multiple' in json_data:
            for table in test_multiple_json['multiple']:
                if 'table' in table and 'data' in table:
                    response.append(upload.post_table(table))
                else:
                    return {
                        'error': 'You must specify a table with data to upload'
                    }
        else:
            if 'table' in json_data and 'data' in json_data:
                response = upload.post_table(test_table_json)
            else:
                return {
                    'error': 'You must specify a table with data to upload'
                }

        if len(response) > 1:
            for res in response:
                if 'error' in res:
                    return {'error': response}
                else:
                    return {'created': response}
        else:
            return response


# Add resource endpoints here =================================================
api.add_resource(Upload, '/upload')
