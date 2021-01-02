from unittest.mock import Mock

import pytest
from flask_jwt_extended import create_refresh_token, decode_token

from app.models.auth import User


@pytest.fixture
def mock_reset_mail(monkeypatch):
    from app.blueprints.api_auth import routes

    mock = Mock()
    monkeypatch.setattr(routes, 'send_password_reset_email', mock)
    return mock


@pytest.mark.parametrize("username, password, code",
                         [('test', 'test', 200),
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


def test_login_user_is_not_admin(test_client, users_set):
    response = test_client.post('/api/auth/login', json={'username': 'test', 'password': 'test'})

    assert response.status_code == 200

    json = response.get_json()
    payload = decode_token(json['access_token'], allow_expired=True)

    assert not payload['user_claims']['is_admin']


def test_login_admin_is_admin(test_client, users_set):
    response = test_client.post('/api/auth/login', json={'username': 'admin', 'password': 'test'})

    assert response.status_code == 200

    json = response.get_json()
    payload = decode_token(json['access_token'], allow_expired=True)

    assert payload['user_claims']['is_admin']


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


def test_login_no_json(test_client, users_set):
    response = test_client.post('/api/auth/login')
    assert response.status_code == 400


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


def test_fresh_login_no_json(test_client, users_set):
    response = test_client.post('/api/auth/fresh-login')
    assert response.status_code == 400


def test_refresh_no_token(test_client, users_set):
    response = test_client.post('/api/auth/refresh')
    assert response.status_code == 401

    json = response.get_json()
    assert not json.get('access_token')
    assert not json.get('refresh_token')


def test_refresh_correct_token(test_client, users_set):
    user1, user2, admin = users_set
    refresh_token = create_refresh_token(identity=user1)

    response = test_client.post('/api/auth/refresh', headers={'Authorization': 'Bearer %s' % refresh_token})
    assert response.status_code == 200

    json = response.get_json()
    assert json.get('access_token')


def test_validate_no_username(test_client, users_set):
    user1, user2, admin = users_set

    response = test_client.post('/api/auth/validate', json={'email': 'sadadfa'})
    assert response.status_code == 200

    json = response.get_json()
    assert json.get('username') is None


def test_validate_no_email(test_client, users_set):
    response = test_client.post('/api/auth/validate', json={'username': 'sadadfa'})
    assert response.status_code == 200

    json = response.get_json()
    assert json.get('email') is None


def test_validate_username_and_email_free(test_client, users_set):
    response = test_client.post('/api/auth/validate', json={'email': 'newtest@test.pl', 'username': 'asdasf'})
    assert response.status_code == 200

    json = response.get_json()
    assert json.get('username').get('checks').get('unique')
    assert json.get('email').get('checks').get('unique')


def test_validate_username_and_email_occupied(test_client, users_set):
    user1, user2, admin = users_set

    response = test_client.post('/api/auth/validate', json={'email': user1.email, 'username': user2.username})
    assert response.status_code == 200

    json = response.get_json()
    assert not json.get('username').get('checks').get('unique')
    assert not json.get('email').get('checks').get('unique')


def test_validate_no_args(test_client, users_set):
    response = test_client.post('/api/auth/validate')
    assert response.status_code == 400


def test_register_occupied_username(test_client, users_set):
    user1, user2, admin = users_set
    response = test_client.post('/api/auth/register',
                                json={'username': user1.username, 'email': 'test12423@test.pl', 'password': 'password'})

    assert response.status_code == 422

    json = response.get_json()
    assert not json.get('username').get('checks').get('unique')


def test_register_occupied_email(test_client, users_set):
    user1, user2, admin = users_set
    response = test_client.post('/api/auth/register',
                                json={'username': 'user1244123', 'email': user1.email, 'password': 'password'})

    assert response.status_code == 422

    json = response.get_json()
    assert not json.get('email').get('checks').get('unique')


def test_register_empty_username(test_client, users_set):
    user1, user2, admin = users_set
    response = test_client.post('/api/auth/register',
                                json={'username': '', 'email': 'test12423@test.pl', 'password': 'password'})

    assert response.status_code == 422

    json = response.get_json()
    assert not json.get('username').get('checks').get('min_length')


def test_register_empty_email(test_client, users_set):
    user1, user2, admin = users_set
    response = test_client.post('/api/auth/register',
                                json={'username': 'user3254234', 'email': '', 'password': 'password'})

    assert response.status_code == 422

    json = response.get_json()
    assert not json.get('email').get('checks').get('min_length')


def test_register_empty_password(test_client, users_set):
    user1, user2, admin = users_set
    response = test_client.post('/api/auth/register',
                                json={'username': 'user3254234', 'email': 'test4324324@test.pl', 'password': ''})

    assert response.status_code == 422

    json = response.get_json()
    assert not json.get('password').get('checks').get('min_length')


def test_register_201(test_client, users_set):
    user1, user2, admin = users_set
    new_user_data = {'username': 'user3254234', 'email': 'test2341234@test.pl', 'password': 'password'}
    response = test_client.post('/api/auth/register', json=new_user_data)

    assert response.status_code == 201

    user = User.query.filter_by(username=new_user_data['username']).first()

    assert user
    assert user.username == new_user_data['username']
    assert user.email == new_user_data['email']


def test_register_no_json(test_client):
    response = test_client.post('/api/auth/register')

    assert response.status_code == 400


def test_reset_password_request_no_json(test_client):
    response = test_client.post('/api/auth/reset_password')

    assert response.status_code == 400


def test_reset_password_request_correct_email(test_client, users_set, mock_reset_mail):
    user1, user2, admin = users_set

    response = test_client.post('/api/auth/reset_password', json={'email': user1.email})

    assert response.status_code == 202
    mock_reset_mail.assert_called_once_with(user1)


def test_reset_password_request_wrong_email(test_client, users_set, mock_reset_mail):
    user1, user2, admin = users_set

    response = test_client.post('/api/auth/reset_password', json={'email': 'test423535@test.com'})

    assert response.status_code == 422
    mock_reset_mail.assert_not_called()


def test_reset_password_no_json(test_client, users_set):
    user1, user2, admin = users_set

    token = user1.get_reset_password_token()
    response = test_client.post('/api/auth/reset_password/' + token)

    assert response.status_code == 400


def test_reset_password_empty_password(test_client, users_set):
    user1, user2, admin = users_set

    token = user1.get_reset_password_token()
    response = test_client.post('/api/auth/reset_password/' + token, json={'password': ''})

    assert response.status_code == 422

    json = response.get_json()
    assert not json.get('password').get('checks').get('min_length')


def test_reset_password_202(test_client, users_set):
    user1, user2, admin = users_set

    token = user1.get_reset_password_token()
    response = test_client.post('/api/auth/reset_password/' + token, json={'password': 'sdadsffsdf'})

    assert response.status_code == 200


def test_reset_password_invalid_token(test_client, users_set):
    user1, user2, admin = users_set

    not_user = User(id=7)

    token = not_user.get_reset_password_token()
    response = test_client.post('/api/auth/reset_password/' + token, json={'password': 'sdadsffsdf'})

    assert response.status_code == 401

    json = response.get_json()
    assert json.get('password') is None  # shouldnt validate password if token is invalid


def test_reset_password_expired_token(test_client, users_set):
    user1, user2, admin = users_set

    token = user1.get_reset_password_token(expires_in=-1000)
    response = test_client.post('/api/auth/reset_password/' + token, json={'password': 'sdadsffsdf'})

    assert response.status_code == 401

    json = response.get_json()
    assert json.get('password') is None
