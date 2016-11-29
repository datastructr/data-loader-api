import pytest
from flask import url_for


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
    ('GET', '/doesnotexist'),
    ('GET', '/api/doesnotexist'),
    ('GET', '/api/v1/doesnotexist'),
))
def test_endpoints_404_status_codes(http_method, http_path, client):
    res = client.open(method=http_method, path=http_path)
    assert res.status_code == 404
