from unittest import TestCase

from app.models import Recipe, User
from app.services import clone_recipe_to_waiting


class TestServices(TestCase):

    def test_clone_recipe_to_waiting_empty(self):
        recipe_model = Recipe()
        waiting_model = clone_recipe_to_waiting(recipe_model)

        self.assertFalse(waiting_model.title)
        self.assertFalse(waiting_model.time)
        self.assertFalse(waiting_model.difficulty)
        self.assertFalse(waiting_model.link)
        self.assertFalse(waiting_model.preparation)
        self.assertFalse(waiting_model.author)
        self.assertEqual(waiting_model.ingredients.count(), 0)

    def test_clone_recipe_to_waiting_full(self):
        user = User(username="test", email="test@test.com")
        recipe_model = Recipe(title='test', time=1, difficulty=1, link='http://test.com', preparation='test',
                              author=user)
        recipe_model.add_ingredient(title='test1', amount=1, unit='kg')
        recipe_model.add_ingredient(title='test2', amount=1, unit='kg')
        waiting_model = clone_recipe_to_waiting(recipe_model)

        self.assertEqual(waiting_model.title, 'test')
        self.assertEqual(waiting_model.time, 1)
        self.assertEqual(waiting_model.difficulty, 1)
        self.assertEqual(waiting_model.link, 'http://test.com')
        self.assertEqual(waiting_model.preparation, 'test')
        self.assertEqual(waiting_model.author, user)
        self.assertEqual(waiting_model.ingredients.count(), 2)
        self.assertEqual(waiting_model.ingredients[0].title, 'test1')
        self.assertEqual(waiting_model.ingredients[0].amount, 1)
        self.assertEqual(waiting_model.ingredients[0].unit, 'kg')
        self.assertEqual(waiting_model.ingredients[1].title, 'test2')
        self.assertEqual(waiting_model.ingredients[1].amount, 1)
        self.assertEqual(waiting_model.ingredients[1].unit, 'kg')

        # TODO: test save z mockupem

        # TODO: test init

        # TODO: testy add_ingredient
