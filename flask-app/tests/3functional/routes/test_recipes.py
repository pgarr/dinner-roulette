import datetime

import pytest


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
                                        last_modified=datetime.datetime(2019, 11, 1),
                                        ingredients=[{'title': 'test1', 'amount': 3, 'unit': 'g'},
                                                     {'title': 'test2', 'amount': 3, 'unit': 'g'}])

    return user1, user2, admin, recipe_model, recipe_model_2, pending_model, refused_model

def test_connection(test_client):
    response = test_client.get('/api/')
    assert response.status_code == 200

