from sqlalchemy import *

# TODO allow for postgis fields (Geometry is needed for current test database)
from geoalchemy2 import Geometry

from app.extensions import db
from app.table_mappings import (
    junction_tables,
    mapping,
)


def get_primary_key(table_name):
    """When given a table return the primary key column name

    :param table_name: The table's name
    :type table_name: String
    :return: String
    """
    metadata = MetaData()

    metadata.reflect(bind=db.engine)

    try:
        table = metadata.tables[table_name]

        for column in table.columns:
            if column.primary_key:
                return str(column.name)
            else:
                continue

    except KeyError:
        return "That table does not exist in the database."


def get_table_headers(table_name):
    """Retrieve and return a single table's header names

    :param table_name: The table_name string to use
    :returns: list of Strings
    """
    if table_name in junction_tables:
        return {'error': 'The schema name you are wishing to GET is not valid'}

    metadata = MetaData()

    metadata.reflect(bind=db.engine)

    try:
        table = metadata.tables[table_name]

        headers = []

        for column in table.columns:
            headers.append(str(column.name))

        if len(headers) == 0:
            return {'error': 'The schema name you are wishing to GET is not valid'}

    except KeyError:
        return {'error': 'The schema name you are wishing to GET is not valid'}

    return headers


def get_single_table(table_name):
    """Retrieve and return a single table's schema

    :param table_name: The table_name string to use
    :returns: dictionary response
    """
    if table_name in junction_tables:
        return {'error': 'The schema name you are wishing to GET is not valid'}

    response = []
    junctions = []

    metadata = MetaData()

    metadata.reflect(bind=db.engine)

    try:
        table = metadata.tables[table_name]

        if table.name in mapping:
            junctions.append({
                'trigger_table': table.name,
                'required_fields': mapping[table.name]['required'],
                'optional_fields': mapping[table.name]['not_required'],
            })

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

        if len(junctions) > 0:

            response.append({
                'table': {
                    'junctions': junctions,
                    'table_properties': properties,
                    'table_name': table.name,
                }
            })

        else:

            response.append({
                'table': {
                    'table_properties': properties,
                    'table_name': table.name
                }
            })

    except KeyError:
        return {'error': 'The schema name you are wishing to GET is not valid'}

    return {'success': response}


def get_tables():
    """Retrieve and return all of a database's table-schema pairs

    :returns: dictionary response
    """

    tables = []
    mappings = []
    hidden_tables = []

    for table in mapping:

        trigger_key = 'trigger_table' in mapping[table]
        require_key = 'required' in mapping[table]
        optional_key = 'not_require' in mapping[table]

        if trigger_key and require_key and optional_key:
            mappings.append({
                'trigger_table': table,
                'required_fields': mapping[table]['required'],
                'optional_fields': mapping[table]['not_required'],
            })
        elif trigger_key and require_key:
            mappings.append({
                'trigger_table': table,
                'required_fields': mapping[table]['required'],
            })
        else:
            return {'error': 'Mapping configuration error'}

        for junction_table in mapping[table]['junction_tables']:
            hidden_tables.append(junction_table)

    metadata = MetaData()

    try:
        metadata.reflect(bind=db.engine)

        for table in metadata.sorted_tables:

            # Do not return the junction tables and their schemas
            if any(table.name == item for item in hidden_tables):
                continue

            properties = []
            junctions = []

            for mapped_table in mappings:
                if table.name in mapped_table['trigger_table']:
                    junctions.append(mapped_table)

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

            if len(junctions) > 0:

                tables.append({
                    'table': {
                        'junctions': junctions,
                        'table_properties': properties,
                        'table_name': table.name,
                    }
                })

            else:

                tables.append({
                    'table': {
                        'table_properties': properties,
                        'table_name': table.name
                    }
                })

    except ConnectionError:
        return {'error': 'Database connection error check configurations'}

    return {'success': tables}
