import requests

from api_tests.base_test import BaseTest


class GetAllRecipesTest(BaseTest):

    def setUp_recipes(self):
        recipes = [
            {"title": "test", "time": 30, "difficulty": 3, "link": "http://test.pl", "preparation": "test test",
             "author": "test2", "ingredients": [
                {"title": "test1", "amount": 3, "unit": "kg"},
                {"title": "test2"}]},
            {"title": "test2", "time": 30, "difficulty": 3, "link": "http://test2.pl", "preparation": "test2 test2",
             "author": "test", "ingredients": [
                {"title": "test1", "amount": 3, "unit": "kg"},
                {"title": "test2"}]}
        ]
        return recipes

    def test_get_all_recipes_all_data(self):
        response = requests.get(self._aut.url + '/api/recipes')
        self.assertEqual(response.status_code, 200, 'Status code')
        print(response.text)

    def test_get_all_recipes_with_user_token(self):
        pass


class GetAllRecipesEmptyTet(BaseTest):
    def test_get_all_recipes_with_empty_lit(self):
        response = requests.get(self._aut.url + '/api/recipes')
        self.assertEqual(response.status_code, 200, 'Status code')
        print(response.text)