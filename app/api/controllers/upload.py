from sqlalchemy import *
from sqlalchemy.exc import SQLAlchemyError

# TODO allow for postgis fields (Geometry is needed for current test database)

from app.extensions import db


def check_data_columns(column_list, data_row):
    """check_data_columns =>> function to take a list of columns that are being
    inserted into (from the data_json) and make sure there are parameters for
    the abstracted insert statement

    :param column_list: list of columns name
    :param data_row: dictionary for a specific ingest row
    :return: dictionary for ingestion
    """
    for item in column_list:
        if item not in data_row:
            column_name = item
            data_row[column_name] = None

    return data_row


def get_data_columns(data_json):
    """get_data_columns =>> generic get 'column' names (keys) from a dictionary

    :param data_json: dictionary of data
    :return: list of column names
    """
    columns = []

    for row in data_json:
        for key in row:
            if key in columns:
                break
            else:
                columns.append(key)

    return columns


def create_abstract_insert(table_name, data_json):
    """create_abstract_insert =>> function to create an abstracted raw insert
    psql statement for inserting a single row of data

    :param table_name: String of a table_name
    :param data_json: dictionary of ingestion data
    :return: String of an insert statement
    """
    table_name = table_name
    data = data_json

    columns = []

    for row in data:
        for key in row:
            if key in columns:
                break
            else:
                columns.append(key)

    values = [':' + item for item in columns]

    values = ', '.join(map(str, values))

    list_columns = ', '.join(map(str, columns))

    statement = 'INSERT INTO ' + str(table_name) + '(' + list_columns + ')' \
        + 'VALUES (' + values + ')'

    return statement


def check_table(table_name, data_json):
    """check_table =>> function that checks whether or not the specified table
    and the columns in that data are valid

    :param table_name: String of the table's name
    :param data_json: the full data ingestion JSON sent through the endpoint
    :return: Boolean
    """
    table_name = table_name
    data = data_json

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
        return 'table: >>' + table_name + '<< was not found'

    for item in columns:
        if item not in check_columns:
            return 'column: >>' + str(item) + '<< was not found in table: >>' + table_name + '<<.'

    return True


# =============================================================================
# Deprecated ==================================================================
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
# End Deprecated ==============================================================
# =============================================================================


def insert_data(table_name, data_json):
    """insert_data =>> function to take in a json object and insert the data
    into the database

    :param table_name: String -> table's name
    :param data_json: json object with rows -> columns -> data
    :return: json response with proper error/success detection
    """

    results = []

    columns = get_data_columns(data_json)

    connection = db.engine.connect()

    transaction = connection.begin()

    try:

        disable_fk_constraints = text('ALTER TABLE %s DISABLE TRIGGER USER' % table_name)

        connection.execute(disable_fk_constraints)

        statement = create_abstract_insert(table_name, data_json)

        insert_sql = text(statement)

        for row in data_json:
            new_row = check_data_columns(columns, row)
            result = connection.execute(insert_sql, **new_row)
            results.append(result)


        transaction.commit()

        enable_fk_constraints = text('ALTER TABLE %s ENABLE TRIGGER USER' % table_name)
        connection.execute(enable_fk_constraints)

    except SQLAlchemyError as e:
        transaction.rollback()

        enable_fk_constraints = text('ALTER TABLE %s ENABLE TRIGGER USER' % table_name)
        connection.execute(enable_fk_constraints)

        return {'insert_error': e}

    return 'successful insert of data into >>' + table_name + '<<'


def post_table(json):
    """post_table =>> function to take a single json object and check -> insert
    the data to a specific table

    :param json: The JSON Object sent to a POST endpoint
    :returns: dictionary response
    """
    rows = []

    if json['data'] is null:
        return {'error': 'You must specify a table with data to upload'}
    else:
        for row in json['data']:
            rows.append(row)

        check = check_table(json['table'], json['data'])

        if check is True:
            result = str(insert_data(json['table'], rows))
            if 'Successful' in result:
                return {'created': result}
            else:
                return {'error': result}
        else:
            return {'error': check}
