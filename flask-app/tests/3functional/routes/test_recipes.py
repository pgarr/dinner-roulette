import datetime

import pytest
from flask import current_app


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


class TestRecipesGet:
    def test_recipes_get(self, test_client, recipes_set):
        response = test_client.get('/api/recipes')
        assert response.status_code == 200

        json = response.get_json()

        assert len(json.get('recipes')) == 2

        required_keys = ("id", "title", "time", "difficulty")
        assert all(keys in json.get("recipes")[0] for keys in required_keys)

    def test_recipes_get_page_1(self, test_client, recipes_set):
        response = test_client.get('/api/recipes', query_string={'page': 1, 'per_page': 1})
        assert response.status_code == 200

        recipes = response.get_json().get('recipes')
        meta = response.get_json().get("_meta")

        assert meta.get('page') == 1
        assert meta.get('total_pages') == 2

        assert len(recipes) == 1
        assert recipes[0].get('id') == 2

    def test_recipes_get_page_2(self, test_client, recipes_set):
        response = test_client.get('/api/recipes', query_string={'page': 2, 'per_page': 1})
        assert response.status_code == 200

        recipes = response.get_json().get('recipes')
        meta = response.get_json().get("_meta")

        assert meta.get('page') == 2
        assert meta.get('total_pages') == 2

        assert len(recipes) == 1
        assert recipes[0].get('id') == 1

    def test_recipes_get_pagination_invalid_page(self, test_client, recipes_set):
        response = test_client.get('/api/recipes', query_string={'page': 'test', 'per_page': 'test'})
        assert response.status_code == 200

        recipes = response.get_json().get('recipes')
        meta = response.get_json().get("_meta")

        assert meta.get('page') == 1
        assert meta.get('per_page') == current_app.config['RECIPES_PER_PAGE']

        assert len(recipes) == 2
