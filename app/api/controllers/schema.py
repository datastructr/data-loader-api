from sqlalchemy import *

# TODO allow for postgis fields (Geometry is needed for current test database)
from geoalchemy2 import Geometry

from app.extensions import db


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
                'table_properties': properties,
                'table_name': table.name
            }
        })

    except KeyError:
        return {'error': KeyError}

    return {'success': response}


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
                'table': {
                    'table_properties': properties,
                    'table_name': table.name
                }
            })

    except ConnectionError:
        return {'error': 'Database connection error check configurations'}

    return {'success': tables}
