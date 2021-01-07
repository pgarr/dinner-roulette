import datetime

import pytest
from flask_jwt_extended import create_access_token

from app import prefix
from app.models.recipes import StatusEnum


@pytest.fixture
def recipes_users_set(ext_users_set, make_recipe):
    user1, user2, user3, admin = ext_users_set
    pending_recipe1 = make_recipe(title='older', time=1, difficulty=1, link='http://test.com', preparation='test',
                                  author=user1, status=StatusEnum.pending,
                                  ingredients=[{'title': 'test1', 'amount': 1, 'unit': 'kg'},
                                               {'title': 'test2', 'amount': 1, 'unit': 'kg'}],
                                  create_date=datetime.datetime(2019, 3, 30),
                                  last_modified=datetime.datetime(2019, 11, 1))
    pending_recipe2 = make_recipe(title='newer', time=2, difficulty=2, link='http://test2.com', preparation='test',
                                  author=user2, status=StatusEnum.pending,
                                  ingredients=[{'title': 'test1', 'amount': 2, 'unit': 'kg'},
                                               {'title': 'test2', 'amount': 2, 'unit': 'dag'}],
                                  create_date=datetime.datetime(2019, 1, 30),
                                  last_modified=datetime.datetime(2019, 12, 1))
    accepted_recipe1 = make_recipe(title='test', time=1, difficulty=1, link='http://test.com', preparation='test',
                                   author=user1, status=StatusEnum.accepted,
                                   ingredients=[{'title': 'test1', 'amount': 1, 'unit': 'kg'},
                                                {'title': 'test2', 'amount': 1, 'unit': 'kg'}])
    accepted_recipe2 = make_recipe(title='test2', time=2, difficulty=2, link='http://test2.com', preparation='test',
                                   author=user2, status=StatusEnum.accepted,
                                   ingredients=[{'title': 'test1', 'amount': 2, 'unit': 'kg'},
                                                {'title': 'test2', 'amount': 2, 'unit': 'dag'}])
    rejected_recipe1 = make_recipe(title='test', time=1, difficulty=1, link='http://test.com', preparation='test',
                                   author=user1, status=StatusEnum.refused,
                                   ingredients=[{'title': 'test1', 'amount': 1, 'unit': 'kg'},
                                                {'title': 'test2', 'amount': 1, 'unit': 'kg'}])
    rejected_recipe2 = make_recipe(title='test2', time=2, difficulty=2, link='http://test2.com', preparation='test',
                                   author=user2, status=StatusEnum.refused,
                                   ingredients=[{'title': 'test1', 'amount': 2, 'unit': 'kg'},
                                                {'title': 'test2', 'amount': 2, 'unit': 'dag'}])

    return user1, user2, user3, admin, pending_recipe1, pending_recipe2, accepted_recipe1, accepted_recipe2, rejected_recipe1, rejected_recipe2


def test_accept_recipe_no_token(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    response = test_client.get(prefix + '/admin/recipes/%d/accept' % pending1.id)
    assert response.status_code == 401


def test_accept_recipe_no_admin(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    token = create_access_token(identity=user1, fresh=True)
    response = test_client.get(prefix + '/admin/recipes/%d/accept' % pending1.id,
                               headers={'Authorization': 'Bearer %s' % token})
    assert response.status_code == 401


def test_accept_recipe_200_when_pending(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    token = create_access_token(identity=admin, fresh=True)
    response = test_client.get(prefix + '/admin/recipes/%d/accept' % pending1.id,
                               headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 200
    recipe = response.get_json().get('recipe')
    assert recipe['status'] == StatusEnum.accepted.name


def test_accept_recipe_200_when_accepted(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    token = create_access_token(identity=admin, fresh=True)
    response = test_client.get(prefix + '/admin/recipes/%d/accept' % accepted1.id,
                               headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 200
    recipe = response.get_json().get('recipe')
    assert recipe['status'] == StatusEnum.accepted.name


def test_accept_recipe_200_when_refused(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    token = create_access_token(identity=admin, fresh=True)
    response = test_client.get(prefix + '/admin/recipes/%d/accept' % rejected1.id,
                               headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 200
    recipe = response.get_json().get('recipe')
    assert recipe['status'] == StatusEnum.accepted.name


def test_accept_recipe_wrong_id(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    not_id = 1111111

    token = create_access_token(identity=admin, fresh=True)
    response = test_client.get(prefix + '/admin/recipes/%d/accept' % not_id,
                               headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 404


def test_reject_recipe_no_token(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    response = test_client.get(prefix + '/admin/recipes/%d/reject' % pending1.id)

    assert response.status_code == 401


def test_reject_recipe_no_admin(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    token = create_access_token(identity=user1, fresh=True)
    response = test_client.get(prefix + '/admin/recipes/%d/reject' % pending1.id,
                               headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 401


def test_reject_recipe_200_when_pending(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    token = create_access_token(identity=admin, fresh=True)
    response = test_client.get(prefix + '/admin/recipes/%d/reject' % pending1.id,
                               headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 200
    recipe = response.get_json().get('recipe')
    assert recipe['status'] == StatusEnum.refused.name


def test_reject_recipe_200_when_accepted(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    token = create_access_token(identity=admin, fresh=True)
    response = test_client.get(prefix + '/admin/recipes/%d/reject' % accepted1.id,
                               headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 200
    recipe = response.get_json().get('recipe')
    assert recipe['status'] == StatusEnum.refused.name


def test_reject_recipe_200_when_refused(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    token = create_access_token(identity=admin, fresh=True)
    response = test_client.get(prefix + '/admin/recipes/%d/reject' % rejected1.id,
                               headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 200
    recipe = response.get_json().get('recipe')
    assert recipe['status'] == StatusEnum.refused.name


def test_reject_recipe_wrong_id(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    not_id = 1111111

    token = create_access_token(identity=admin, fresh=True)
    response = test_client.get(prefix + '/admin/recipes/%d/reject' % not_id,
                               headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 404


def test_pending_recipes_no_token(test_client, recipes_users_set):
    response = test_client.get(prefix + '/admin/recipes/pending')

    assert response.status_code == 401


def test_pending_recipes_no_admin(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    token = create_access_token(identity=user1, fresh=True)
    response = test_client.get(prefix + '/admin/recipes/pending', headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 401


def test_pending_recipes_200(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    token = create_access_token(identity=admin, fresh=True)
    response = test_client.get(prefix + '/admin/recipes/pending', headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 200
    recipes = response.get_json().get('recipes')
    assert len(recipes) == 2


def test_pending_recipes_sorted_from_oldest_updated(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    token = create_access_token(identity=admin, fresh=True)
    response = test_client.get(prefix + '/admin/recipes/pending', headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 200
    recipes = response.get_json().get('recipes')
    assert len(recipes) == 2

    assert recipes[0]['title'] == 'older'
    assert recipes[1]['title'] == 'newer'
