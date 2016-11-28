"""
Unit tests for controllers/upload.py

TODO: some of the function connect to databases
    ( so implement spin up/tear down function ) for later database tests
"""
from app.api.controllers import upload


def test_create_abstract_junction_insert():
    one = 'INSERT INTO leads_countries(lead_fid, country_id)VALUES (:lead_fid, :country_id)'
    two = 'INSERT INTO leads_countries(country_id, lead_fid)VALUES (:country_id, :lead_fid)'

    assert upload.create_abstract_junction_insert('leads', 'leads_countries') == one \
        or upload.create_abstract_junction_insert('leads', 'leads_countries') == two


def test_validate_junction_data(valid_data_json):
    assert upload.validate_junction_data('leads', valid_data_json) is True


def test_post_table():
    """Testing out the else constraints on post_table method
    """

    # no ``table`` key in JSON
    bad_table = {
        "no_table_key": "",
    }
    # no ``data`` key in JSON
    bad_data = {
        "table": "table",
        "no_data_key": "",
    }
    # no table String in JSON
    no_table = {
        "table": "",
    }
    # no data values in JSON
    no_data = {
        "table": "some_table",
        "data": "",
    }

    # json tests
    assert upload.post_table(bad_table) == \
        {'error': 'You must have the \'table\' key in your JSON object'}
    assert upload.post_table(bad_data) == \
        {'error': 'You must have the \'data\' key in your JSON object'}
    assert upload.post_table(no_table) == \
        {'error': 'You must specify a table with data to upload'}
    assert upload.post_table(no_data) == \
        {'error': 'You must enter data allocated with your table'}
