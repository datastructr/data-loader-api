import pytest
from app import create_app


# BIDS Specific JSON DATA =====================================================
@pytest.fixture(scope='module')
def valid_data_json():
    """This is a JSON Object for the ``data`` but in a Dictionary syntax that
    will be used throughout testing methods
    :return: A JSON type of Object with keys and data for the API to handle
    :returns: JSON Object
    """
    return [
        {
            "project_title": "tátle_1",
            "project_number": "1",
            "project_size": "1000000",
            "project_description": "description_1",
            "country_name": "United Kingdom",
            "sector": "Finance and Insurance",
        },
        {
            "project_title": "select * from leads;",
            "project_number": "2",
            "project_size": "10000",
            "project_description": "description_2",
            "country_name": "Austria",
            "sector": "Other",
        },
        {
            "project_title": "title_3",
            "project_number": "3",
            "project_size": "1",
            "project_description": "description_3",
            "country_name": "Egypt",
            "sector": "Utilities",
            "test_name": "Test One",
        },
    ]


@pytest.fixture(scope='module')
def valid_row_json():
    """This is a JSON Object for the ``data`` but in a Dictionary syntax that
    will be used throughout testing methods
    :return: A JSON type of Object with keys and data for the API to handle
    :returns: JSON Object
    """
    return {
        "project_title": "title_3",
        "project_number": "3",
        "project_size": "1",
        "project_description": "description_3",
    }


@pytest.fixture(scope='module')
def valid_json():
    """This is a JSON Object but in a Dictionary syntax that will be used
    throughout testing methods
    :return: A JSON type of Object with keys and data for the API to handle
    :returns: JSON Object
    """
    return {
        "table": "leads",
        "data": [
            {
                "project_title": "tátle_1",
                "project_number": "1",
                "project_size": "1000000",
                "project_description": "description_1",
                "country_name": "United Kingdom",
                "sector": "Finance and Insurance",
            },
            {
                "project_title": "select * from leads;",
                "project_number": "2",
                "project_size": "10000",
                "project_description": "description_2",
                "country_name": "Austria",
                "sector": "Other",
            },
            {
                "project_title": "title_3",
                "project_number": "3",
                "project_size": "1",
                "project_description": "description_3",
                "country_name": "Egypt",
                "sector": "Utilities",
                "test_name": "Test One",
            },
        ],
        "junction_fields": [
            "country_name",
            "sector",
            "test_name",
        ]
    }
# End of BIDS Specific JSON DATA ==============================================


@pytest.fixture(scope='module')
def app(request):
    """Creates a flask.Flask app with the 'development' config/context.
    :request: test request
    :returns: flask.Flask object
    """

    app = create_app('development')
    ctx = app.app_context()

    ctx.push()

    def tear_down():
        ctx.pop()

    request.addfinalizer(tear_down)
    return app


@pytest.fixture
def client(app):
    """Creates a flask.Flask test_client object
    :app: fixture that provided the flask.Flask app
    :returns: flask.Flask test_client object
    """

    return app.test_client()
