from flask import json

from app import db
from app.models import RecipeDetail, Recipe, RecipeIngredient
from tests.base_test import TestAppSetUp


def create_sample_recipe(name, *ingredient_names):
    recipe_detail_model = RecipeDetail(
        link='http://test',
        description='test'
    )
    recipe_model = Recipe(
        name=name,
        detail=recipe_detail_model,
        ingredients=[]
    )
    for ingredient_name in ingredient_names:
        recipe_ingredient_model = RecipeIngredient(
            name=ingredient_name,
            amount=1,
            unit='test'
        )
        recipe_model.ingredients.append(recipe_ingredient_model)
    return recipe_model


class TestRoutes(TestAppSetUp):

    def test_connection(self):
        with self.app.test_client() as c:
            r = c.get('/api/')
            self.assertEqual(200, r.status_code)
            self.assertEqual({'message': 'API is online!'}, json.loads(r.get_data()))

    def test_get_recipes_empty_list(self):
        with self.app.test_client() as c:
            r = c.get('/api/recipes')
            self.assertEqual(200, r.status_code)
            self.assertEqual({'recipes': []}, json.loads(r.get_data()))

    def test_get_recipes_list(self):
        db.session.add(create_sample_recipe('test1', 'name1', 'name2'))

        with self.app.test_client() as c:
            r = c.get('/api/recipes')
        self.assertEqual(200, r.status_code)
        self.assertEqual({'recipes': [{'id': 1, 'name': 'test1'}]}, json.loads(r.get_data()))

    def test_get_recipes_filtered_empty_list(self):
        db.session.add(create_sample_recipe('test1', 'name1', 'name2'))

        with self.app.test_client() as c:
            r = c.get('/api/recipes?ingredient=test')
        self.assertEqual(200, r.status_code)
        self.assertEqual({'recipes': []}, json.loads(r.get_data()))

    def test_get_recipes_filtered_list(self):
        db.session.add(create_sample_recipe('test1', 'name1', 'name2'))
        db.session.add(create_sample_recipe('test2', 'name11', 'name22'))

        with self.app.test_client() as c:
            r = c.get('/api/recipes?ingredient=name22')
        self.assertEqual(200, r.status_code)
        self.assertEqual({'recipes': [{'id': 2, 'name': 'test2'}]}, json.loads(r.get_data()))

    def test_get_recipe_id(self):
        db.session.add(create_sample_recipe('test1', 'name1', 'name2'))
        db.session.add(create_sample_recipe('test2', 'name11', 'name22'))

        with self.app.test_client() as c:
            r = c.get('/api/recipe/2')
        self.assertEqual(200, r.status_code)
        self.assertEqual(
            {'recipe':
                 {'detail':
                      {'description': 'test',
                       'id': 2,
                       'link': 'http://test'},
                  'id': 2,
                  'ingredients': [{'amount': 1,
                                   'calories': None,
                                   'id': 3,
                                   'name': 'name11',
                                   'unit': 'test'},
                                  {'amount': 1,
                                   'calories': None,
                                   'id': 4,
                                   'name': 'name22',
                                   'unit': 'test'}],
                  'name': 'test2'}},
            json.loads(r.get_data()))

    def test_get_recipe_id_not_exist(self):
        db.session.add(create_sample_recipe('test1', 'name1', 'name2'))
        db.session.add(create_sample_recipe('test2', 'name11', 'name22'))

        with self.app.test_client() as c:
            r = c.get('/api/recipe/3')
        self.assertEqual(404, r.status_code)
        self.assertEqual({'message': 'Recipe could not be found.'}, json.loads(r.get_data()))

    def test_post_recipe_no_data(self):
        with self.app.test_client() as c:
            r = c.post('/api/recipe')
            self.assertEqual(400, r.status_code)
            self.assertEqual({'message': 'No input data provided'}, json.loads(r.get_data()))

    def test_post_recipe_none_name(self):
        with self.app.test_client() as c:
            r = c.post('/api/recipe', json={
                "name": None,
                "ingredients": [
                    {"name": "papryka", "amount": 1, "unit": "sztuka"},
                    {"name": "bułka", "amount": 1, "unit": "sztuka"}
                ],
                "detail": {
                    "link": "http://0",
                    "description": "test description"
                }
            })
            self.assertEqual(422, r.status_code)
            self.assertEqual({'name': ['Field may not be null.']}, json.loads(r.get_data()))

    def test_post_recipe_empty_ingredients(self):
        with self.app.test_client() as c:
            r = c.post('/api/recipe', json={
                "name": "test1",
                "ingredients": [],
                "detail": {
                    "link": "http://0",
                    "description": "test description"
                }
            })
            self.assertEqual(422, r.status_code)
            self.assertEqual({'ingredients': ['Data not provided.']}, json.loads(r.get_data()))

    def test_post_recipe_none_detail(self):
        with self.app.test_client() as c:
            r = c.post('/api/recipe', json={
                "name": "test1",
                "ingredients": [
                    {"name": "papryka", "amount": 1, "unit": "sztuka"},
                    {"name": "bułka", "amount": 1, "unit": "sztuka"}
                ],
                "detail": None
            })
            self.assertEqual(422, r.status_code)
            self.assertEqual({'detail': ['Field may not be null.']}, json.loads(r.get_data()))

    def test_post_recipe(self):
        with self.app.test_client() as c:
            r = c.post('/api/recipe', json={
                "name": "test1",
                "ingredients": [
                    {"name": "papryka", "amount": 1, "unit": "sztuka"},
                    {"name": "bułka", "amount": 1, "unit": "sztuka"}
                ],
                "detail": {
                    "link": "http://0",
                    "description": "test description"
                }
            })
            self.assertEqual(201, r.status_code)
            self.assertEqual({'message': 'Created new recipe.',
                              'recipe':
                                  {'detail':
                                       {'description': 'test description',
                                        'id': 1,
                                        'link': 'http://0'},
                                   'id': 1,
                                   'ingredients': [{'amount': 1,
                                                    'calories': None,
                                                    'id': 1,
                                                    'name': 'papryka',
                                                    'unit': 'sztuka'},
                                                   {'amount': 1,
                                                    'calories': None,
                                                    'id': 2,
                                                    'name': 'bułka',
                                                    'unit': 'sztuka'}],
                                   'name': 'test1'}},
                             json.loads(r.get_data()))
            recipe = Recipe.query.get(1)
            self.assertEqual('test1', recipe.name)
            self.assertEqual('test description', recipe.detail.description)
            self.assertEqual('http://0', recipe.detail.link)
            self.assertTrue(any(ingredient.name == 'papryka' for ingredient in recipe.ingredients))
            self.assertTrue(any(ingredient.name == 'bułka' for ingredient in recipe.ingredients))
