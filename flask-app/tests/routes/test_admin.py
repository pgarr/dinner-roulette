import datetime

import pytest
from flask_jwt_extended import create_access_token


@pytest.fixture
def recipes_set(users_set, make_recipe, make_waiting_recipe):
    user1, user2, admin = users_set

    pending_model = make_waiting_recipe(title='test3', time=3, difficulty=3, link='http://test3.com',
                                        preparation='test3',
                                        author=user1, create_date=datetime.datetime(2019, 1, 30),
                                        last_modified=datetime.datetime(2019, 11, 1),
                                        ingredients=[{'title': 'test1', 'amount': 3, 'unit': 'g'},
                                                     {'title': 'test2', 'amount': 3, 'unit': 'g'}])

    refused_model = make_waiting_recipe(title='test4', time=4, difficulty=4, link='http://test4.com',
                                        preparation='test4',
                                        author=user2, create_date=datetime.datetime(2019, 1, 30),
                                        last_modified=datetime.datetime(2019, 11, 1), refused=True,
                                        ingredients=[{'title': 'test1', 'amount': 3, 'unit': 'g'},
                                                     {'title': 'test2', 'amount': 3, 'unit': 'g'}])

    return user1, user2, admin, pending_model, refused_model


def test_accept_recipe_no_token(test_client, recipes_set):
    user1, user2, admin, pending_model, refused_model = recipes_set

    response = test_client.get('/api/admin/waiting/%d/accept' % pending_model.id)
    assert response.status_code == 401


def test_accept_recipe_no_admin(test_client, recipes_set):
    user1, user2, admin, pending_model, refused_model = recipes_set

    token = create_access_token(identity=user1, fresh=True)
    response = test_client.get('/api/admin/waiting/%d/accept' % pending_model.id,
                               headers={'Authorization': 'Bearer %s' % token})
    assert response.status_code == 401


def test_accept_recipe_ok(test_client, recipes_set):
    user1, user2, admin, pending_model, refused_model = recipes_set

    token = create_access_token(identity=admin, fresh=True)
    response = test_client.get('/api/admin/waiting/%d/accept' % pending_model.id,
                               headers={'Authorization': 'Bearer %s' % token})
    assert response.status_code == 200


def test_accept_recipe_wrong_id(test_client, recipes_set):
    user1, user2, admin, pending_model, refused_model = recipes_set

    not_id = 1111111

    token = create_access_token(identity=admin, fresh=True)
    response = test_client.get('/api/admin/waiting/%d/accept' % not_id, headers={'Authorization': 'Bearer %s' % token})
    assert response.status_code == 404


def test_reject_recipe_no_token(test_client, recipes_set):
    user1, user2, admin, pending_model, refused_model = recipes_set

    response = test_client.get('/api/admin/waiting/%d/reject' % pending_model.id)
    assert response.status_code == 401


def test_reject_recipe_no_admin(test_client, recipes_set):
    user1, user2, admin, pending_model, refused_model = recipes_set

    token = create_access_token(identity=user1, fresh=True)
    response = test_client.get('/api/admin/waiting/%d/reject' % pending_model.id,
                               headers={'Authorization': 'Bearer %s' % token})
    assert response.status_code == 401


def test_reject_recipe_ok(test_client, recipes_set):
    user1, user2, admin, pending_model, refused_model = recipes_set

    token = create_access_token(identity=admin, fresh=True)
    response = test_client.get('/api/admin/waiting/%d/reject' % pending_model.id,
                               headers={'Authorization': 'Bearer %s' % token})
    assert response.status_code == 200


def test_reject_recipe_wrong_id(test_client, recipes_set):
    user1, user2, admin, pending_model, refused_model = recipes_set

    not_id = 1111111

    token = create_access_token(identity=admin, fresh=True)
    response = test_client.get('/api/admin/waiting/%d/reject' % not_id, headers={'Authorization': 'Bearer %s' % token})
    assert response.status_code == 404
