import pytest


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


def test_login_no_password(test_client, users_set):
    username = 'test'
    response = test_client.post('/api/auth/login', json={'username': username})
    assert response.status_code == 401


def test_login_no_username(test_client, users_set):
    password = 'test'
    response = test_client.post('/api/auth/login', json={'password': password})
    assert response.status_code == 401