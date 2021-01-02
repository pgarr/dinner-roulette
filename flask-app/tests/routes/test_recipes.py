import datetime

import pytest
from flask import current_app
from flask_jwt_extended import create_access_token

from app.models.auth import User


@pytest.fixture
def recipes_set(users_set, make_recipe, make_waiting_recipe):
    user1, user2, admin = users_set

    recipe_model = make_recipe(title='test', time=1, difficulty=1, link='http://test.com', preparation='test',
                               author=user1, create_date=datetime.datetime(2019, 1, 30),
                               last_modified=datetime.datetime(2019, 11, 1),
                               ingredients=[{'title': 'test1', 'amount': 1, 'unit': 'kg'},
                                            {'title': 'test2', 'amount': 1, 'unit': 'kg'}])
    recipe_model_2 = make_recipe(title='test2', time=2, difficulty=2, link='http://test2.com', preparation='test',
                                 author=user2, create_date=datetime.datetime(2019, 1, 30),
                                 last_modified=datetime.datetime(2019, 11, 1),
                                 ingredients=[{'title': 'test1', 'amount': 2, 'unit': 'kg'},
                                              {'title': 'test2', 'amount': 2, 'unit': 'dag'}])
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

    return user1, user2, admin, recipe_model, recipe_model_2, pending_model, refused_model


def test_connection(test_client):
    response = test_client.get('/api/')
    assert response.status_code == 200


def test_recipes_get(test_client, recipes_set):
    response = test_client.get('/api/recipes')
    assert response.status_code == 200

    json = response.get_json()

    assert len(json.get('recipes')) == 2

    required_keys = ("id", "title", "time", "difficulty")
    assert all(keys in json.get("recipes")[0] for keys in required_keys)


def test_recipes_get_page_1(test_client, recipes_set):
    response = test_client.get('/api/recipes', query_string={'page': 1, 'per_page': 1})
    assert response.status_code == 200

    recipes = response.get_json().get('recipes')
    meta = response.get_json().get("_meta")

    assert meta.get('page') == 1
    assert meta.get('total_pages') == 2

    assert len(recipes) == 1
    assert recipes[0].get('id') == 2


def test_recipes_get_page_2(test_client, recipes_set):
    response = test_client.get('/api/recipes', query_string={'page': 2, 'per_page': 1})
    assert response.status_code == 200

    recipes = response.get_json().get('recipes')
    meta = response.get_json().get("_meta")

    assert meta.get('page') == 2
    assert meta.get('total_pages') == 2

    assert len(recipes) == 1
    assert recipes[0].get('id') == 1


def test_recipes_get_pagination_invalid_page(test_client, recipes_set):
    response = test_client.get('/api/recipes', query_string={'page': 'test', 'per_page': 'test'})
    assert response.status_code == 200

    recipes = response.get_json().get('recipes')
    meta = response.get_json().get("_meta")

    assert meta.get('page') == 1
    assert meta.get('per_page') == current_app.config['RECIPES_PER_PAGE']

    assert len(recipes) == 2


def test_create_recipe_no_token(test_client, recipes_set):
    response = test_client.post('/api/recipe', json={})
    assert response.status_code == 401


def test_create_recipe_invalid_token(test_client, recipes_set):
    not_user = User(id=7)

    token = create_access_token(identity=not_user, fresh=True)
    response = test_client.post('/api/recipe', headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 401


def test_create_recipe_no_data(test_client, recipes_set):
    user1, user2, admin, recipe_model, recipe_model_2, pending_model, refused_model = recipes_set

    token = create_access_token(identity=user1, fresh=True)
    response = test_client.post('/api/recipe', headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 400


def test_create_recipe_no_title(test_client, recipes_set):
    user1, user2, admin, recipe_model, recipe_model_2, pending_model, refused_model = recipes_set

    recipe_json = {'ingredients': []}

    token = create_access_token(identity=user1, fresh=True)
    response = test_client.post('/api/recipe', json=recipe_json, headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 422
    assert response.get_json().get('title')


@pytest.mark.parametrize("title, amount, unit",
                         [('test', '', 'a'),
                          ('test', '1', 'a'),
                          ('test', '1.2', 'a'),
                          ('test', None, ''),
                          ('test', 1, ''),
                          ('test', 1.2, '')])
def test_create_recipe_ingredients_formats_ok(test_client, recipes_set, title, amount, unit):
    user1, user2, admin, recipe_model, recipe_model_2, pending_model, refused_model = recipes_set

    recipe_json = {'title': 'qwert', 'ingredients': [{'title': title, 'amount': amount, 'unit': unit}]}

    token = create_access_token(identity=user1, fresh=True)
    response = test_client.post('/api/recipe', json=recipe_json, headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 201

    ingredient_data = response.get_json().get('pending_recipe').get('ingredients')[0]

    assert ingredient_data.get('title') == title
    assert ingredient_data.get('amount') == (float(amount) if amount else '')
    assert ingredient_data.get('unit') == unit


def test_create_recipe_correct_data_saved(test_client, recipes_set):
    user1, user2, admin, recipe_model, recipe_model_2, pending_model, refused_model = recipes_set
    title = 'test'
    time = 15
    difficulty = 4
    link = 'http://test.pl'
    preparation = 'qwerty asdfg zxcv 123 ąćęłóńśźż'
    ingredients = []

    recipe_json = {'title': title, 'time': time, 'difficulty': difficulty, 'link': link, 'preparation': preparation,
                   'ingredients': ingredients}

    token = create_access_token(identity=user1, fresh=True)
    response = test_client.post('/api/recipe', json=recipe_json, headers={'Authorization': 'Bearer %s' % token})

    assert response.status_code == 201
    data = response.get_json().get('pending_recipe')

    assert data.get('title') == title
    assert data.get('time') == time
    assert data.get('difficulty') == difficulty
    assert data.get('link') == link
    assert data.get('preparation') == preparation
    assert data.get('ingredients') == ingredients

    assert data.get('author') == user1.username
