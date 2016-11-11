from sqlalchemy import *
from sqlalchemy import text

# TODO allow for postgis fields (Geometry is needed for current test database)
from geoalchemy2 import Geometry

from app.extensions import db
from app.utils import (
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


# TODO : refactor this and create_values to be one function to reduce time
#   complexity
def create_insert(row):
    """create_insert =>> function to add the columns to an import statement

    :param row: dictionary -> of column data
    :return: String
    """
    statement = ''
    length = len(row)
    index = 0
    for item in row:
        if index == length - 1:
            statement += str(item) + ')'
        else:
            index += 1
            statement += str(item) + ', '

    return statement


# TODO : refactor this and create_insert to be one function to reduce time
#   complexity
def create_values(row):
    """create_values =>> function to add the values to an import statement

    :param row: dictionary -> of column data
    :return: String
    """
    statement = ' VALUES ('
    length = len(row)
    index = 0
    for item in row:
        if index == length - 1:
            statement += '\'' + str(row.get(item)) + '\')'
        else:
            index += 1
            statement += '\'' + str(row.get(item)) + '\', '

    return statement


def insert_row(statement):
    """insert_row =>> function to insert a row of data into the database

    :param statement: String -> insert statement for a specific row
    :return: response database raised error or successful result
    """
    try:
        result = db.engine.execute(statement)
    except:
        # return abort_database_insert_error(statement)
        raise

    return result


def insert_data(table_name, data_json):
    """insert_data =>> function to take in a json object and insert the data
    into the database

    :param table_name: String -> table's name
    :param data_json: json object with rows -> columns -> data
    :return: json response with proper error/success detection
    """

    inserts = []

    for row in data_json:
        # start sql statement
        stmt = 'INSERT INTO ' + table_name + ' ('

        insert_into_stmt = create_insert(row)

        values = create_values(row)

        sql = text(stmt + insert_into_stmt + values)

        inserts.append(sql)

    for i in inserts:
        try:
            insert_row(i)
        except:
            raise

    return {'message': 'Successful insert of data into ' + table_name}


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
            return insert_data(json['table'], rows)
        else:
            return check
