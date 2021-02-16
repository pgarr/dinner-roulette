import datetime

import pytest
from flask import current_app
from flask_jwt_extended import create_access_token

from app import prefix
from app.models.user import User
from app.models.recipe import StatusEnum


@pytest.fixture
def recipes_users_set(ext_users_set, make_recipe):
    user1, user2, user3, admin = ext_users_set
    pending_recipe1 = make_recipe(title='test', time=1, difficulty=1, link='http://test.com', preparation='test',
                                  author=user1, status=StatusEnum.pending,
                                  ingredients=[{'title': 'test1', 'amount': 1, 'unit': 'kg'},
                                               {'title': 'test2', 'amount': 1, 'unit': 'kg'}])
    pending_recipe2 = make_recipe(title='test2', time=2, difficulty=2, link='http://test2.com', preparation='test',
                                  author=user2, status=StatusEnum.pending,
                                  ingredients=[{'title': 'test1', 'amount': 2, 'unit': 'kg'},
                                               {'title': 'test2', 'amount': 2, 'unit': 'dag'}])
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


def assert_ingredient_data(ingredient_data, title, amount, unit):
    assert ingredient_data.get('title') == title
    assert ingredient_data.get('amount') == (float(amount) if amount else '')
    assert ingredient_data.get('unit') == unit


def test_connection(test_client):
    response = test_client.get(prefix + '/')
    assert response.status_code == 200


def test_recipes_get(test_client, recipes_users_set):
    response = test_client.get(prefix + '/recipes')
    assert response.status_code == 200

    json = response.get_json()

    assert len(json.get('recipes')) == 2

    required_keys = ("id", "title", "time", "difficulty")
    assert all(keys in json.get("recipes")[0] for keys in required_keys)


def test_recipes_get_page_1(test_client, recipes_users_set):
    response = test_client.get(prefix + '/recipes', query_string={'page': 1, 'per_page': 1})
    assert response.status_code == 200

    recipes = response.get_json().get('recipes')
    meta = response.get_json().get("_meta")

    assert meta.get('page') == 1
    assert meta.get('total_pages') == 2

    assert len(recipes) == 1
    assert recipes[0].get('id') == 4


def test_recipes_get_page_2(test_client, recipes_users_set):
    response = test_client.get(prefix + '/recipes', query_string={'page': 2, 'per_page': 1})
    assert response.status_code == 200

    recipes = response.get_json().get('recipes')
    meta = response.get_json().get("_meta")

    assert meta.get('page') == 2
    assert meta.get('total_pages') == 2

    assert len(recipes) == 1
    assert recipes[0].get('id') == 3


def test_recipes_get_pagination_invalid_page(test_client, recipes_users_set):
    response = test_client.get(prefix + '/recipes', query_string={'page': 'test', 'per_page': 'test'})
    assert response.status_code == 200

    recipes = response.get_json().get('recipes')
    meta = response.get_json().get("_meta")

    assert meta.get('page') == 1
    assert meta.get('per_page') == current_app.config['RECIPES_PER_PAGE']

    assert len(recipes) == 2


def test_my_recipes_get_no_token(test_client, recipes_users_set):
    response = test_client.get(prefix + '/recipes/my')
    assert response.status_code == 401


def test_my_recipes_get_invalid_token(test_client, recipes_users_set):
    not_user = User(id=7)

    token = create_access_token(identity=not_user, fresh=True)
    response = test_client.get(prefix + '/recipes/my', headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 401


def test_my_recipes_get_200(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    token = create_access_token(identity=user1, fresh=True)
    response = test_client.get(prefix + '/recipes/my', headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 200
    recipes = response.get_json().get('recipes')
    assert len(recipes) == 3


def test_my_recipes_get_all_has_status(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    token = create_access_token(identity=user1, fresh=True)
    response = test_client.get(prefix + '/recipes/my', headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 200
    recipes = response.get_json().get('recipes')
    assert all('status' in recipe for recipe in recipes)


def test_my_recipes_get_200_but_no_recipes(test_client, recipes_users_set, make_user):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    token = create_access_token(identity=user3, fresh=True)
    response = test_client.get(prefix + '/recipes/my', headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 200
    recipes = response.get_json().get('recipes')
    assert len(recipes) == 0


def test_recipe_get_wrong_id(test_client, recipes_users_set):
    response = test_client.get(prefix + '/recipes/12345')

    assert response.status_code == 404


def test_recipe_get_pending_no_token_should_401(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    response = test_client.get(prefix + '/recipes/%d' % pending1.id)

    assert response.status_code == 401


def test_recipe_get_refused_no_token_should_401(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    response = test_client.get(prefix + '/recipes/%d' % rejected1.id)

    assert response.status_code == 401


def test_recipe_get_accepted_should_200(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    response = test_client.get(prefix + '/recipes/%d' % accepted1.id)

    assert response.status_code == 200
    recipe = response.get_json().get('recipe')

    assert recipe.get('id') == accepted1.id


def test_recipe_get_accepted_author_should_200(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    token = create_access_token(identity=user1, fresh=True)
    response = test_client.get(prefix + '/recipes/%d' % accepted1.id, headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 200
    recipe = response.get_json().get('recipe')

    assert recipe.get('id') == accepted1.id


def test_recipe_get_accepted_admin_should_200(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    token = create_access_token(identity=admin, fresh=True)
    response = test_client.get(prefix + '/recipes/%d' % accepted1.id, headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 200
    recipe = response.get_json().get('recipe')

    assert recipe.get('id') == accepted1.id


def test_recipe_get_accepted_not_author_should_200(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    token = create_access_token(identity=user2, fresh=True)
    response = test_client.get(prefix + '/recipes/%d' % accepted1.id, headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 200
    recipe = response.get_json().get('recipe')

    assert recipe.get('id') == accepted1.id


def test_recipe_get_pending_author_should_200(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    token = create_access_token(identity=user1, fresh=True)
    response = test_client.get(prefix + '/recipes/%d' % pending1.id, headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 200
    recipe = response.get_json().get('recipe')

    assert recipe.get('id') == pending1.id


def test_recipe_get_pending_admin_should_200(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    token = create_access_token(identity=admin, fresh=True)
    response = test_client.get(prefix + '/recipes/%d' % pending1.id, headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 200
    recipe = response.get_json().get('recipe')

    assert recipe.get('id') == pending1.id


def test_recipe_get_pending_not_author_should_401(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    token = create_access_token(identity=user2, fresh=True)
    response = test_client.get(prefix + '/recipes/%d' % pending1.id, headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 401


def test_recipe_get_refused_author_should_200(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    token = create_access_token(identity=user1, fresh=True)
    response = test_client.get(prefix + '/recipes/%d' % rejected1.id, headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 200
    recipe = response.get_json().get('recipe')

    assert recipe.get('id') == rejected1.id


def test_recipe_get_refused_admin_should_200(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    token = create_access_token(identity=admin, fresh=True)
    response = test_client.get(prefix + '/recipes/%d' % rejected1.id, headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 200
    recipe = response.get_json().get('recipe')

    assert recipe.get('id') == rejected1.id


def test_recipe_get_refused_not_author_should_401(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    token = create_access_token(identity=user2, fresh=True)
    response = test_client.get(prefix + '/recipes/%d' % rejected1.id, headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 401


def test_create_recipe_no_token(test_client, recipes_users_set):
    response = test_client.post(prefix + '/recipes', json={})
    assert response.status_code == 401


def test_create_recipe_invalid_token(test_client, recipes_users_set):
    not_user = User(id=7)

    token = create_access_token(identity=not_user, fresh=True)
    response = test_client.post(prefix + '/recipes', json={}, headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 401


def test_create_recipe_no_data(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    token = create_access_token(identity=user1, fresh=True)
    response = test_client.post(prefix + '/recipes', headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 400


def test_create_recipe_no_title(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    recipe_json = {'ingredients': []}

    token = create_access_token(identity=user1, fresh=True)
    response = test_client.post(prefix + '/recipes', json=recipe_json, headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 422
    assert response.get_json().get('title')


@pytest.mark.parametrize("title, amount, unit",
                         [('test', '', 'a'),
                          ('test', '1', 'a'),
                          ('test', '1.2', 'a'),
                          ('test', None, ''),
                          ('test', 1, ''),
                          ('test', 1.2, '')])
def test_create_recipe_ingredients_formats_ok(test_client, recipes_users_set, title, amount, unit):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    recipe_json = {'title': 'qwert', 'ingredients': [{'title': title, 'amount': amount, 'unit': unit}]}

    token = create_access_token(identity=user1, fresh=True)
    response = test_client.post(prefix + '/recipes', json=recipe_json, headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 201

    ingredient_data = response.get_json().get('recipe').get('ingredients')[0]

    assert_ingredient_data(ingredient_data, title, amount, unit)


def test_create_recipe_correct_data_saved(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    title = 'test'
    time = 15
    difficulty = 4
    link = 'http://test.pl'
    preparation = 'qwerty asdfg zxcv 123 ąćęłóńśźż'
    ingredients = []

    recipe_json = {'title': title, 'time': time, 'difficulty': difficulty, 'link': link, 'preparation': preparation,
                   'ingredients': ingredients}

    token = create_access_token(identity=user1, fresh=True)
    response = test_client.post(prefix + '/recipes', json=recipe_json, headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 201
    data = response.get_json().get('recipe')

    assert data['title'] == title
    assert data['time'] == time
    assert data['difficulty'] == difficulty
    assert data['link'] == link
    assert data['preparation'] == preparation
    assert data['ingredients'] == ingredients

    assert data['author'] == user1.username


def test_create_recipe_status_is_pending(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    title = 'test'
    time = 15
    difficulty = 4
    link = 'http://test.pl'
    preparation = 'qwerty asdfg zxcv 123 ąćęłóńśźż'
    ingredients = []

    recipe_json = {'title': title, 'time': time, 'difficulty': difficulty, 'link': link, 'preparation': preparation,
                   'ingredients': ingredients}

    token = create_access_token(identity=user1, fresh=True)
    response = test_client.post(prefix + '/recipes', json=recipe_json, headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 201
    data = response.get_json().get('recipe')

    assert data['status'] == StatusEnum.pending.name


def test_update_recipe_correct_data_saved(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    title = 'test'
    time = 15
    difficulty = 4
    link = 'http://test.pl'
    preparation = 'qwerty asdfg zxcv 123 ąćęłóńśźż'
    ingredients = []

    recipe_json = {'title': title, 'time': time, 'difficulty': difficulty, 'link': link, 'preparation': preparation,
                   'ingredients': ingredients}

    token = create_access_token(identity=user1, fresh=True)
    response = test_client.patch(prefix + '/recipes/%d' % accepted1.id, json=recipe_json,
                                 headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 200
    data = response.get_json().get('recipe')

    assert data['title'] == title
    assert data['time'] == time
    assert data['difficulty'] == difficulty
    assert data['link'] == link
    assert data['preparation'] == preparation
    assert data['ingredients'] == ingredients

    assert data['author'] == user1.username


def test_update_recipe_no_data(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    token = create_access_token(identity=user1, fresh=True)

    response = test_client.patch(prefix + '/recipes/%d' % accepted1.id,
                                 headers={'Authorization': 'Bearer %s' % token})
    assert response.status_code == 400


def test_update_recipe_no_token(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    response = test_client.patch(prefix + '/recipes/%d' % accepted1.id, json={})
    assert response.status_code == 401


def test_update_recipe_invalid_token(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    not_user = User(id=7)

    token = create_access_token(identity=not_user, fresh=True)
    response = test_client.patch(prefix + '/recipes/%d' % accepted1.id, json={},
                                 headers={'Authorization': 'Bearer %s' % token})
    assert response.status_code == 401


def test_update_recipe_invalid_user(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    recipe_json = {'ingredients': [], 'title': 'test'}
    token = create_access_token(identity=user2, fresh=True)
    response = test_client.patch(prefix + '/recipes/%d' % accepted1.id, json=recipe_json,
                                 headers={'Authorization': 'Bearer %s' % token})
    assert response.status_code == 401


def test_update_recipe_no_title(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    recipe_json = {'ingredients': []}

    token = create_access_token(identity=user1, fresh=True)
    response = test_client.patch(prefix + '/recipes/%d' % accepted1.id, json=recipe_json,
                                 headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 422
    assert response.get_json().get('title')


@pytest.mark.parametrize("title, amount, unit",
                         [('test', '', 'a'),
                          ('test', '1', 'a'),
                          ('test', '1.2', 'a'),
                          ('test', None, ''),
                          ('test', 1, ''),
                          ('test', 1.2, '')])
def test_update_recipe_ingredients_formats_ok(test_client, recipes_users_set, title, amount, unit):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    recipe_json = {'title': 'qwert', 'ingredients': [{'title': title, 'amount': amount, 'unit': unit}]}

    token = create_access_token(identity=user1, fresh=True)
    response = test_client.patch(prefix + '/recipes/%d' % accepted1.id, json=recipe_json,
                                 headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 200

    ingredient_data = response.get_json().get('recipe').get('ingredients')[0]

    assert_ingredient_data(ingredient_data, title, amount, unit)


def test_update_recipe_resets_status(test_client, recipes_users_set):
    user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

    title = 'test'
    time = 15
    difficulty = 4
    link = 'http://test.pl'
    preparation = 'qwerty asdfg zxcv 123 ąćęłóńśźż'
    ingredients = []

    recipe_json = {'title': title, 'time': time, 'difficulty': difficulty, 'link': link, 'preparation': preparation,
                   'ingredients': ingredients}

    token = create_access_token(identity=user1, fresh=True)
    response = test_client.patch(prefix + '/recipes/%d' % accepted1.id, json=recipe_json,
                                 headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 200
    data = response.get_json().get('recipe')

    assert data['status'] == StatusEnum.pending.name
