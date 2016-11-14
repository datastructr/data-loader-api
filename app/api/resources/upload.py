from flask_restful import Resource, request

from app.api import api
from app.api.controllers import upload
from app.utils import abort_bad_upload_json

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
    def post(self):
        json_data = request.get_json(force=True)

        response = []
        if 'multiple' in json_data:
            for table in json_data['multiple']:
                if 'table' in table and 'data' in table:
                    response.append(upload.post_table(table))
                else:
                    return abort_bad_upload_json()
        else:
            if 'table' in json_data and 'data' in json_data:
                response = upload.post_table(json_data)
            else:
                return abort_bad_upload_json()

        return response


# Add resource endpoints here =================================================
api.add_resource(Upload, '/upload')
