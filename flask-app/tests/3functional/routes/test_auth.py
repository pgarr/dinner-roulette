import pytest
from flask_jwt_extended import create_refresh_token


@pytest.mark.parametrize("username, password, code", [('test', 'test', 200),
                                                      ('addadas', 'test', 401),
                                                      ('test', 'safdfaa', 401),
                                                      ('test', '', 401),
                                                      ('', 'test', 401),
                                                      ('test', 'Test', 401),
                                                      ('test', 'teSt', 401),
                                                      ('test', 'test ', 401),
                                                      ('TEST', 'test', 401),
                                                      ('Test', 'test', 401)])
def test_login(test_client, users_set, username, password, code):
    response = test_client.post('/api/auth/login', json={'username': username, 'password': password})
    assert response.status_code == code

    json = response.get_json()
    if code == 401:
        assert not json.get('access_token')
        assert not json.get('refresh_token')
    if code == 200:
        assert json.get('access_token')
        assert json.get('refresh_token')


def test_login_no_password(test_client, users_set):
    username = 'test'
    response = test_client.post('/api/auth/login', json={'username': username})
    assert response.status_code == 401

    json = response.get_json()
    assert not json.get('access_token')
    assert not json.get('refresh_token')


def test_login_no_username(test_client, users_set):
    password = 'test'
    response = test_client.post('/api/auth/login', json={'password': password})
    assert response.status_code == 401

    json = response.get_json()
    assert not json.get('access_token')
    assert not json.get('refresh_token')


@pytest.mark.parametrize("username, password, code", [('test', 'test', 200),
                                                      ('addadas', 'test', 401),
                                                      ('test', 'safdfaa', 401),
                                                      ('test', '', 401),
                                                      ('', 'test', 401),
                                                      ('test', 'Test', 401),
                                                      ('test', 'teSt', 401),
                                                      ('test', 'test ', 401),
                                                      ('TEST', 'test', 401),
                                                      ('Test', 'test', 401)])
def test_fresh_login(test_client, users_set, username, password, code):
    response = test_client.post('/api/auth/fresh-login', json={'username': username, 'password': password})
    assert response.status_code == code

    json = response.get_json()
    if code == 401:
        assert not json.get('access_token')
        assert not json.get('refresh_token')
    if code == 200:
        assert json.get('access_token')
        assert not json.get('refresh_token')


def test_fresh_login_no_password(test_client, users_set):
    username = 'test'
    response = test_client.post('/api/auth/fresh-login', json={'username': username})
    assert response.status_code == 401

    json = response.get_json()
    assert not json.get('access_token')
    assert not json.get('refresh_token')


def test_fresh_login_no_username(test_client, users_set):
    password = 'test'
    response = test_client.post('/api/auth/fresh-login', json={'password': password})
    assert response.status_code == 401

    json = response.get_json()
    assert not json.get('access_token')
    assert not json.get('refresh_token')


def test_refresh_no_token(test_client, users_set):
    response = test_client.post('/api/auth/refresh')
    assert response.status_code == 401

    json = response.get_json()
    assert not json.get('access_token')
    assert not json.get('refresh_token')


def test_refresh_correct_token(test_client, users_set):
    user1, user2, admin = users_set
    refresh_token = create_refresh_token(identity=user1.username)

    response = test_client.post('/api/auth/refresh', headers={'Authorization': 'Bearer %s' % refresh_token})
    assert response.status_code == 200

    json = response.get_json()
    assert json.get('access_token')
