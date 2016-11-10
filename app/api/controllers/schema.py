from sqlalchemy import *

# TODO allow for postgis fields (Geometry is needed for current test database)
from geoalchemy2 import Geometry

from app.extensions import db
from app.utils import (
    abort_bad_endpoint,
    abort_bad_upload_json,
    abort_column_not_found,
    abort_table_not_found,
)


def check_table(table_json):
    """check_table =>> function that checks whether or not the specified table
    and the columns in that data are valid

    :param table_json: the full table JSON sent through the endpoint
    :return: Boolean
    """
    table_name = table_json['table']
    data = table_json['data']

    columns = []

    for row in data:
        for key in row:
            if key in columns:
                break
            else:
                columns.append(key)

    metadata = MetaData()

    metadata.reflect(bind=db.engine)

    check_columns = []

    try:
        table = metadata.tables[table_name]

        for column in table.columns:
            check_columns.append(str(column.name))
    except LookupError:
        return abort_table_not_found(table_name)

    for item in columns:
        if item not in check_columns:
            return abort_column_not_found(item, table_name)

    return True


def insert_data(data_json):
    return {'message': 'hello in insert_data'}


def get_single_table(table_name):
    """get_single_table =>> function to retrieve and return a
    single table's schema

    :param table_name: The table_name string to use
    :returns: dictionary response
    """
    response = []

    metadata = MetaData()

    metadata.reflect(bind=db.engine)

    try:
        table = metadata.tables[table_name]

        properties = []

        for column in table.columns:
            foreign_keys = []

            for key in column.foreign_keys:
                foreign_keys.append(key.target_fullname)

            properties.append({
                'foreign_keys': foreign_keys,
                'primary_key': column.primary_key,
                'nullable': str(column.nullable),
                'type': str(column.type),
                'column': str(column.name)
            })

        response.append({
            'table': {
                'properties': properties,
                'name': table.name
            }
        })

    except KeyError:
        return abort_bad_endpoint()

    return response


def get_tables():
    """get_table =>> function to retrieve and return all of a
    database's table-schema pairs

    :returns: dictionary response
    """
    tables = []

    metadata = MetaData()

    try:
        metadata.reflect(bind=db.engine)

        for table in metadata.sorted_tables:
            properties = []

            for column in table.columns:
                foreign_keys = []

                for key in column.foreign_keys:
                    foreign_keys.append(key.target_fullname)

                properties.append({
                    'foreign_keys': foreign_keys,
                    'primary_key': column.primary_key,
                    'nullable': str(column.nullable),
                    'type': str(column.type),
                    'column': str(column.name)
                })

            tables.append({
                'table' : {
                    'properties': properties,
                    'name': table.name
                }
            })

    except ConnectionError:
        return abort_bad_endpoint()

    return tables


def post_table(json):
    """post_table =>> function to take a single json object and check -> insert
    the data to a specific table

    :param json: The JSON Object sent to a POST endpoint
    :returns: dictionary response
    """
    rows = []

    if json['data'] is null:
        return abort_bad_upload_json()
    else:
        for row in json['data']:
            rows.append(row)

        check = check_table(json)

        if check is True:
            # print(rows)
            return insert_data(rows)
        else:
            return check
