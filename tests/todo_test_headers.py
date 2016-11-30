import collections
import json
import pytest
from app import helpers


standardize_api_response_valid_scenarios = [
    [
        lambda response: {'success': response},
        (json.dumps(collections.OrderedDict([
            ('status_code', 200),
            ('description', 'Successful Operation'),
            ('data', 'foo'),
            ])), 200)
    ],
    [
        lambda response: {'error': response},
        (json.dumps(collections.OrderedDict([
            ('status_code', 400),
            ('error', 'Bad Request'),
            ('data', 'foo'),
            ])), 400)
    ],
    [
        lambda response: {'created': response},
        (json.dumps(collections.OrderedDict([
            ('status_code', 201),
            ('description', 'Successfully created'),
            ('data', 'foo'),
            ])), 201)
    ],
    [
        lambda response: {'updated': response},
        (json.dumps(collections.OrderedDict([
            ('status_code', 200),
            ('description', 'Successfully updated'),
            ('data', 'foo'),
            ])), 200)
    ],
    [
        lambda response: {'no-data': response},
        (json.dumps(collections.OrderedDict([
            ('status_code', 204),
            ('description', ''),
            ('data', ''),
            ])), 204)
    ]
]


def test_standardize_api_response_invalid_result_key():

    fake_controller = lambda *args, **kwargs: {'invalid': ''}  # noqa

    with pytest.raises(ValueError) as error:
        helpers.api_response(fake_controller)('foo')
    assert str(error.value) == 'Invalid result key.'


@pytest.mark.parametrize(
    'function, expected',
    standardize_api_response_valid_scenarios
)
def test_standardize_api_response_valid_result_key(function, expected):
    result = helpers.api_response(function)(response='foo')
    assert result == expected
