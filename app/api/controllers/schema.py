from sqlalchemy import *

# TODO allow for postgis fields
from geoalchemy2 import Geometry

from app.extensions import db
from app.utils import abort_404


def getColumns(table_name):
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


def getSingleTable(table_name):
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


# retrieve all the tables and columns/properties and return a dictionary of metadata
def getTables():
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

# TODO insert data into a table based on json object being passed through
def postTables(data):
    table = data['table']

    columns = getColumns(table)

    for column, value in data['data']:
        print('column...  \n', column)
        print('     value...  \n', value)

    # with engine.begin() as connection:
    #     r1 = connection.execute('INSERT INTO ' + data.table.table_name + ' VALUES (' )
    #     connection.execute(table1.insert(), col1=7, col2='this is some data')
