import json
import pytest
from flask import url_for

from tests.utils import json_request


def test_upload_api_endpoint(accept_json, client):
    res = client.get(url_for('api.upload'), headers=accept_json)
    assert res.mimetype == 'application/json'


def test_schema_api_endpoint(accept_json, client):
    res = client.get(url_for('api.schemalist'), headers=accept_json)
    assert res.mimetype == 'application/json'


@pytest.mark.parametrize('http_method, http_path', (
    ('GET', '/api/v1/schema'),
    ('GET', '/api/v1/schema/accounts'),
    ('POST', '/api/v1/upload'),
))
def test_endpoints_mimetypes(http_method, http_path, client):
    res = client.open(method=http_method, path=http_path)
    assert res.mimetype == 'application/json'


@pytest.mark.parametrize('http_method, http_path', (
    ('GET', '/api/v1/schema'),
    ('GET', '/api/v1/schema/accounts'),
    ('GET', '/api/v1/schema/answers'),
    ('GET', '/api/v1/schema/countries'),
    ('GET', '/api/v1/schema/leads'),
    ('GET', '/api/v1/schema/sectors'),
    ('GET', '/api/v1/schema/tests'),
))
def test_endpoints_200_status_codes(http_method, http_path, client):
    res = client.open(method=http_method, path=http_path)
    assert res.status_code == 200


@pytest.mark.parametrize('http_method, http_path', (
    ('GET', '/api/v1/schema/notreal1'),
    ('GET', '/api/v1/schema/notreal2'),
    ('GET', '/api/v1/schema/notreal3'),
))
def test_400_get_request(http_method, http_path, client):
    response = json_request(method=http_method, url=http_path, client=client)
    response = json.loads(response.data.decode('utf-8'))

    expected = {
        'status_code': 400,
        'data': 'The schema name you are wishing to GET is not valid',
        'error': 'Bad Request',
    }

    assert sorted(response.items()) == sorted(expected.items())


@pytest.mark.parametrize('http_method, http_path', (
    ('GET', '/api/v1/schema'),
    ('GET', '/api/v1/schema/accounts'),
    ('GET', '/api/v1/schema/answers'),
    ('GET', '/api/v1/schema/countries'),
    ('GET', '/api/v1/schema/leads'),
    ('GET', '/api/v1/schema/sectors'),
    ('GET', '/api/v1/schema/tests'),
))
def test_200_get_request(http_method, http_path, client):
    response = json_request(method=http_method, url=http_path, client=client)
    response = json.loads(response.data.decode('utf-8'))

    assert response['status_code'] == 200
    assert response['description'] == 'Successful Operation'
