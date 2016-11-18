import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError

# TODO allow for postgis fields (Geometry is needed for current test database)

from app.extensions import db
from app.table_mappings import mapping


def create_abstract_junction_insert(table_name, junction_table_name):
    """create_abstract_junction_insert =>> function to create an abstracted
    parameters based insertion into a junction table

    :param table_name: String table name hooked with a junction insert
    :param junction_table_name: String junction table's name
    :return: String of an insert statement
    """
    columns = []

    if 'junction_tables' in mapping[table_name]:
        if junction_table_name in mapping[table_name]['junction_tables']:
            if 'columns' in mapping[table_name]['junction_tables'][junction_table_name]:
                for column, value in mapping[table_name]['junction_tables'][junction_table_name]['columns'].items():
                    columns.append(column)
            else:
                return {
                    'error': 'Upload failed columns are required in mapping'
                             ' configuration'
                }
        else:
            return {
                'error': 'Upload failed due to missing junction table: '
                         + junction_table_name
            }
    else:
        return {
            'error': 'Upload failed due to missing junction'
                     ' tables mapping configurations.'
        }

    values = [':' + item for item in columns]

    values = ', '.join(map(str, values))

    list_columns = ', '.join(map(str, columns))

    statement = 'INSERT INTO ' + str(junction_table_name) + '(' + \
                list_columns + ')' + 'VALUES (' + values + ')'

    return statement


def get_junctions_foreign_key(table_name, column_name, column_value):
    """get_junctions_foreign_key =>> function that will select from a table in
    the database to get a primary key to insert into the junction table

    :param table_name: String table name hooked with a junction insert
    :param column_name: String column name where clause will have
    :param column_value: Unique value in the table so you can get a primary key
        for junction insertions
    :return: dictionary response
    """
    key_selectors = 'selectors' in mapping[table_name]
    key_junctions = 'junction_tables' in mapping[table_name]

    if key_selectors and key_junctions:

        if column_name in mapping[table_name]['selectors']:

            junction_table = mapping[table_name]['selectors'][column_name]

            if any(junction_table in table
                   for table in mapping[table_name]['junction_tables']):

                table_cond = 'mapped_table' in mapping[table_name]['junction_tables'][junction_table]
                field_cond = 'mapped_field' in mapping[table_name]['junction_tables'][junction_table]

                if table_cond and field_cond:

                    select_table = mapping[table_name]['junction_tables'][junction_table]['mapped_table']
                    select_field = mapping[table_name]['junction_tables'][junction_table]['mapped_field']

                    select_table_check = select_table is None
                    select_field_check = select_field is None

                    if select_table_check or select_field_check:
                        return {
                            'error': 'You must have values for mapped keys'
                        }

                    value = None

                    select_stmt = sqlalchemy.text(
                                    'SELECT ' + select_field +
                                    ' FROM ' + select_table +
                                    ' WHERE ' + column_name +
                                    ' = \'' + column_value + '\''
                                )

                    try:
                        result = db.engine.execute(select_stmt)
                        for row in result:
                            value = row[select_field]
                    except SQLAlchemyError as e:
                        return {
                            'selection_error': e
                        }

                    return {
                        'junction_table': junction_table,
                        'value': value,
                    }

                else:
                    return {
                        'error': 'Invalid mapping configuration. Missing '
                        + ' mapped configurations.'
                    }
            else:
                return {
                    'error': 'Invalid mapping configuration. Missing '
                    + 'junction table: ' + str(junction_table)
                }
        else:
            return {
                'error': 'Invalid mapping configuration. Missing column name: '
                + str(column_name)
            }
    else:
        return {
            'error': 'Invalid mapping configurations '
                     'make sure you have selectors and junction_tables '
                     'assigned to correct values'
        }


def validate_junction_data(table_name, data_json):
    """validate_junction_data =>> function to take the data JSON and determine
    whether or not it's a valid ingestion set (must pass required fields)

    :param table_name: String of a table's name
    :param data_json: dictionary of all the ingestion data for a table
    :return: BOOLEAN
    """

    junction_fields = []

    # get all of the junction fields to validate junction data
    if 'required' in mapping[table_name]:
        if mapping[table_name]['required'] is not None:
            for element in mapping[table_name]['required']:
                junction_fields.append(element)

    if 'not_required' in mapping[table_name]:
        if mapping[table_name]['not_required'] is not None:
            for element in mapping[table_name]['not_required']:
                junction_fields.append(element)

    row_count = 0
    column_count = 0

    for row in data_json:
        for key, value in row.items():
            if key in junction_fields:
                if value is None or value == '':
                    return 'The value in row: ' + str(row_count) +  \
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


def get_hooked_table_id(table_name, junction_table_name):
    """get_hooked_table_id =>> function to return the mapped primary unique id
    to "RETURN" it's value after insert

    :param table_name: String table name hooked with a junction insert
    :param junction_table_name: String junction table's name
    :return: String of column name
    """
    if junction_table_name in mapping[table_name]['junction_tables']:
        for column, value in \
                mapping[table_name]['junction_tables'][junction_table_name]['columns'].items():
            if table_name in value:
                return value[table_name]


def create_abstract_insert(table_name, data_json, return_field):
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

    if return_field is not None:
        statement = 'INSERT INTO ' + str(table_name) + '(' + list_columns + ')' \
            + 'VALUES (' + values + ') RETURNING ' + str(return_field)
    else:
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
                return 'column: >>' + str(item) + '<< was not found in table: >>'\
                       + table_name + '<<.'
        else:
            if item not in check_columns:
                return 'column: >>' + str(item) + '<< was not found in table: >>'\
                       + table_name + '<<.'

    return True


def insert_data(table_name, data_json):
    """insert_data =>> function to take in a json object and insert the data
    into the database

    :param table_name: String -> table's name
    :param data_json: json object with rows -> columns -> data
    :return: json response with proper error/success detection
    """

    if table_name in mapping:
        junction_fields = []

        check_junction_data = validate_junction_data(table_name, data_json)

        if 'required' in mapping[table_name]:
            if mapping[table_name]['required'] is not None:
                for element in mapping[table_name]['required']:
                    junction_fields.append(element)

        if 'not_required' in mapping[table_name]:
            if mapping[table_name]['not_required'] is not None:
                for element in mapping[table_name]['not_required']:
                    junction_fields.append(element)

        if check_junction_data is True:
            # keep going with the upload
            print('I am inserting table data that has a hook for junction inserts')

            columns = get_data_columns(data_json)

            for row in data_json:

                new_row = check_data_columns(columns, row)

                junction_inserts = []
                return_column = None

                for column, value in new_row.items():

                    junction_insert = None

                    if column in junction_fields \
                            and value is not None:
                        junction_object = get_junctions_foreign_key(table_name, column, value)

                        junction_insert = \
                            create_abstract_junction_insert(
                                table_name,
                                junction_object['junction_table']
                            )

                        return_column = get_hooked_table_id(
                            table_name,
                            junction_object['junction_table']
                        )

                    if junction_insert is not None:
                        junction_inserts.append(junction_insert)

                if return_column is not None:
                    statement = create_abstract_insert(table_name, data_json, return_column)
                    print(statement)
                    for insert in junction_inserts:
                        print(insert)

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
