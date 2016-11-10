from sqlalchemy import *

# TODO allow for postgis fields (Geometry is needed for current test database)
from geoalchemy2 import Geometry

from app.extensions import db
from app.utils import abort_404


# unused function right now
def get_columns(table_name):
    columns = []

    metadata = MetaData()

    metadata.reflect(bind=db.engine)

    try:
        table = metadata.tables[table_name]

        for column in table.columns:
            columns.append({
                'primary_key': column.primary_key,
                'column_name': str(column.name),
                'type': str(column.type),
                'nullable': str(column.nullable),
            })

    except LookupError:
        return abort_404()

    return columns


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
            properties.append({
                'primary_key': column.primary_key,
                'nullable': str(column.nullable),
                'type': str(column.type),
                'column_name': str(column.name)
            })

        response.append({
            'table': {
                'properties': properties,
                'name': table.name
            }
        })

    except KeyError:
        return abort_404()

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
                properties.append({
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
        return abort_404()

    return tables


def post_table(json):
    """get_single_table function

    :param json: The JSON Object sent to a POST endpoint
    :returns: dictionary response
    """
    rows = []

    if json['data'] is null:
        return abort_404()
    else:
        for column in json['data']:
            for key in column:
                rows.append({key: column[key]})

        print(rows)

    return {'message': 'You have successfully uploaded data to the >>' \
                       + json['table'] + '<< table'}
