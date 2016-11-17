import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError

# TODO allow for postgis fields (Geometry is needed for current test database)

from app.extensions import db
from app.table_mappings import mapping


def validate_junction_data(table_name, data_json):
    """validate_junction_data =>> function to take the data JSON and determine
    whether or not it's a valid ingestion set (must pass required fields)

    :param table_name: String of a table's name
    :param data_json: dictionary of all the ingestion data for a table
    :return: BOOLEAN
    """

    # no need to validate the 'required' key it's already there
    required_fields = mapping[table_name]['required']
    not_required_fields = mapping[table_name]['not_required']

    row_count = 0
    column_count = 0

    for row in data_json:
        for key, value in row.items():
            if key in required_fields:
                if value is None or value == '':
                    return 'The value in row: ' + str(row_count) +  \
                                 ' column: ' + str(column_count) + ' must be valid.'
            elif key in not_required_fields:
                if value is None or value == '':
                    return 'The value in row: ' + str(row_count) + \
                                 ' column: ' + str(column_count) + ' must be valid.'

            column_count += 1

        column_count = 0
        row_count += 1

    return True


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
    junction_columns = []

    # if the table has junction hooks on it disregard the junction columns
    if 'required' in mapping[table_name]:
        if mapping[table_name]['required'] is not None:
            for element in mapping[table_name]['required']:
                junction_columns.append(element)

    if 'not_required' in mapping[table_name]:
        if mapping[table_name]['not_required'] is not None:
            for element in mapping[table_name]['not_required']:
                junction_columns.append(element)

    print(junction_columns)

    for row in data:
        for key in row:
            if key in columns:
                continue
            else:
                columns.append(key)

    metadata = sqlalchemy.MetaData()

    metadata.reflect(bind=db.engine)

    check_columns = []

    try:
        table = metadata.tables[table_name]

        for column in table.columns:
            check_columns.append(str(column.name))
    except LookupError:
        return 'table: >>' + table_name + '<< was not found'

    for item in columns:
        # if there are junction hooks check disregard columns for junctions
        if len(junction_columns) > 0:
            if item not in check_columns and item not in junction_columns:
                return 'column: >>' + str(item) + '<< was not found in table: >>' + table_name + '<<.'
        else:
            if item not in check_columns:
                return 'column: >>' + str(item) + '<< was not found in table: >>' + table_name + '<<.'

    return True


def insert_data(table_name, data_json):
    """insert_data =>> function to take in a json object and insert the data
    into the database

    :param table_name: String -> table's name
    :param data_json: json object with rows -> columns -> data
    :return: json response with proper error/success detection
    """

    if table_name in mapping:
        check_junction_data = validate_junction_data(table_name, data_json)

        if check_junction_data is True:
            # keep going with the upload
            print('I am inserting table data that has a hook for junction inserts')
        else:
            return check_junction_data
    else:
        print('I am not inserting table data that has a hook for junction inserts')
        results = []

        columns = get_data_columns(data_json)

        connection = db.engine.connect()

        transaction = connection.begin()

        try:

            disable_fk_constraints = sqlalchemy.text('ALTER TABLE %s DISABLE TRIGGER USER' % table_name)

            connection.execute(disable_fk_constraints)

            statement = create_abstract_insert(table_name, data_json)

            insert_sql = sqlalchemy.text(statement)

            for row in data_json:
                new_row = check_data_columns(columns, row)
                result = connection.execute(insert_sql, **new_row)
                results.append(result)

            transaction.commit()

            enable_fk_constraints = sqlalchemy.text('ALTER TABLE %s ENABLE TRIGGER USER' % table_name)
            connection.execute(enable_fk_constraints)

        except SQLAlchemyError as e:
            transaction.rollback()

            enable_fk_constraints = sqlalchemy.text('ALTER TABLE %s ENABLE TRIGGER USER' % table_name)
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

    if 'table' in json:
        if json['table'] is None or json['table'] == '':
            return {'error': 'You must specify a table with data to upload'}

    if 'data' in json:
        if json['data'] is None or json['data'] == '':
            return {'error': 'You must enter data allocated with your table'}
        else:
            for row in json['data']:
                rows.append(row)

            check = check_table(json['table'], json['data'])

            if check is True:
                result = str(insert_data(json['table'], rows))
                if 'successful' in result:
                    return {'created': result}
                else:
                    return {'error': result}
            else:
                return {'error': check}
