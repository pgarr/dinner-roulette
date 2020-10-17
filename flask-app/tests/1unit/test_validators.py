import pytest

import app
from app.validators import validate_email, validate_username, validate_password


def occupied(param):
    return True


def free(param):
    return None


@pytest.fixture
def username_free(monkeypatch):
    monkeypatch.setattr(app.validators, 'get_user_by_name', free)


@pytest.fixture
def username_occupied(monkeypatch):
    monkeypatch.setattr(app.validators, 'get_user_by_name', occupied)


@pytest.fixture
def email_free(monkeypatch):
    monkeypatch.setattr(app.validators, 'get_user_by_email', free)


@pytest.fixture
def email_occupied(monkeypatch):
    monkeypatch.setattr(app.validators, 'get_user_by_email', occupied)


def test_validate_email_ok(email_free):
    email = 'test@test.pl'
    is_valid, check_dict = validate_email(email)
    assert is_valid


def test_validate_email_no_at(email_free):
    email = 'testtest.pl'
    is_valid, check_dict = validate_email(email)
    assert not is_valid
    assert not check_dict['format']


def test_validate_email_no_dot(email_free):
    email = 'test@testpl'
    is_valid, check_dict = validate_email(email)
    assert not is_valid
    assert not check_dict['format']


def test_validate_email_empty(email_free):
    email = ''
    is_valid, check_dict = validate_email(email)
    assert not is_valid
    assert not check_dict['format']


def test_validate_email_not_unique(email_occupied):
    email = 'test@test.pl'
    is_valid, check_dict = validate_email(email)
    assert not is_valid
    assert not check_dict['unique']


def test_validate_username_ok(username_free):
    username = 'test'
    is_valid, check_dict = validate_username(username)
    assert is_valid


def test_validate_username_not_unique(username_occupied):
    username = 'test'
    is_valid, check_dict = validate_username(username)
    assert not is_valid
    assert not check_dict['unique']


def test_validate_username_empty(username_free):
    username = ''
    is_valid, check_dict = validate_username(username)
    assert not is_valid
    assert not check_dict['min_length']


def test_validate_password_empty():
    password = ''
    is_valid, check_dict = validate_password(password)
    assert not is_valid
    assert not check_dict['min_length']


def test_validate_password_ok():
    password = 'adsadasdasd'
    is_valid, check_dict = validate_password(password)
    assert is_valid
