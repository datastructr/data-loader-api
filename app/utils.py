"""
Utility functions used throughout the application
"""
from flask_restful import abort


def abort_bad_endpoint():
    abort(404, message='That end point does not exist')


def abort_bad_upload_json():
    abort(404, message='You must specify a table with data to upload')


def abort_table_not_found(table_name):
    abort(404, message='Table >' + table_name + '< was not found')


def abort_column_not_found(column_name, table_name):
    return {'message': 'Column >' + column_name + '< was not found in >' + table_name + '<.'}


def abort_database_insert_error(row):
    abort(400, message='Insert error: failed at statement -->' + row)
