from unittest import TestCase

from app.models import Recipe, User, WaitingRecipe, RecipeIngredient, WaitingRecipeIngredient
from app.services import clone_recipe_to_waiting, init_waiting_recipe, _push_updates_to_recipe


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
                              author=user, ingredients=[RecipeIngredient(title='test1', amount=1, unit='kg'),
                                                        RecipeIngredient(title='test2', amount=1, unit='kg')])
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

    def test_init_waiting_recipe_all_data(self):
        user = User(username="test", email="test@test.com")
        waiting_model = init_waiting_recipe(title='test', time=1, difficulty=1, link='http://test.com',
                                            preparation='test',
                                            author=user)

        self.assertEqual(waiting_model.title, 'test')
        self.assertEqual(waiting_model.time, 1)
        self.assertEqual(waiting_model.difficulty, 1)
        self.assertEqual(waiting_model.link, 'http://test.com')
        self.assertEqual(waiting_model.preparation, 'test')
        self.assertEqual(waiting_model.author, user)
        self.assertEqual(waiting_model.ingredients.count(), 0)

    def test_init_waiting_recipe_empty_data(self):
        waiting_model = init_waiting_recipe()

        self.assertFalse(waiting_model.title)
        self.assertFalse(waiting_model.time)
        self.assertFalse(waiting_model.difficulty)
        self.assertFalse(waiting_model.link)
        self.assertFalse(waiting_model.preparation)
        self.assertFalse(waiting_model.author)
        self.assertEqual(waiting_model.ingredients.count(), 0)

    def test_push_updates_to_recipe_new_recipe_full_data(self):
        user = User(username="test", email="test@test.com")
        waiting_model = WaitingRecipe(title='test', time=1, difficulty=1, link='http://test.com', preparation='test',
                                      author=user,
                                      ingredients=[WaitingRecipeIngredient(title='test1', amount=1, unit='kg'),
                                                   WaitingRecipeIngredient(title='test2', amount=1, unit='kg')])
        recipe_model = _push_updates_to_recipe(waiting_model)

        self.assertFalse(recipe_model.id)
        self.assertEqual(recipe_model.title, 'test')
        self.assertEqual(recipe_model.time, 1)
        self.assertEqual(recipe_model.difficulty, 1)
        self.assertEqual(recipe_model.link, 'http://test.com')
        self.assertEqual(recipe_model.preparation, 'test')
        self.assertEqual(recipe_model.author, user)
        self.assertEqual(recipe_model.ingredients.count(), 2)
        self.assertEqual(recipe_model.ingredients[0].title, 'test1')
        self.assertEqual(recipe_model.ingredients[0].amount, 1)
        self.assertEqual(recipe_model.ingredients[0].unit, 'kg')
        self.assertEqual(recipe_model.ingredients[1].title, 'test2')
        self.assertEqual(recipe_model.ingredients[1].amount, 1)
        self.assertEqual(recipe_model.ingredients[1].unit, 'kg')

    def test_push_updates_to_recipe_update_recipe_full_data(self):
        user = User(username="test", email="test@test.com")
        recipe_model = Recipe(id=1, title='testold', time=15, difficulty=3, link='http://testold.com',
                              preparation='testold',
                              author=user,
                              ingredients=[RecipeIngredient(title='test1old', amount=21, unit='g'),
                                           RecipeIngredient(title='test2', amount=1, unit='kg')])
        waiting_model = WaitingRecipe(title='test', time=1, difficulty=1, link='http://test.com', preparation='test',
                                      author=user,
                                      ingredients=[WaitingRecipeIngredient(title='test1', amount=1, unit='kg'),
                                                   WaitingRecipeIngredient(title='test2', amount=1, unit='kg')],
                                      updated_recipe=recipe_model)
        recipe_model = _push_updates_to_recipe(waiting_model)

        self.assertEqual(recipe_model.id, 1)
        self.assertEqual(recipe_model.title, 'test')
        self.assertEqual(recipe_model.time, 1)
        self.assertEqual(recipe_model.difficulty, 1)
        self.assertEqual(recipe_model.link, 'http://test.com')
        self.assertEqual(recipe_model.preparation, 'test')
        self.assertEqual(recipe_model.author, user)
        self.assertEqual(recipe_model.ingredients.count(), 2)
        self.assertEqual(recipe_model.ingredients[0].title, 'test1')
        self.assertEqual(recipe_model.ingredients[0].amount, 1)
        self.assertEqual(recipe_model.ingredients[0].unit, 'kg')
        self.assertEqual(recipe_model.ingredients[1].title, 'test2')
        self.assertEqual(recipe_model.ingredients[1].amount, 1)
        self.assertEqual(recipe_model.ingredients[1].unit, 'kg')

    def test_push_updates_to_recipe_new_recipe_minimal_data(self):
        user = User(username="test", email="test@test.com")
        waiting_model = WaitingRecipe(title='test',
                                      author=user)
        recipe_model = _push_updates_to_recipe(waiting_model)

        self.assertFalse(recipe_model.id)
        self.assertEqual(recipe_model.title, 'test')
        self.assertFalse(recipe_model.time)
        self.assertFalse(recipe_model.difficulty)
        self.assertFalse(recipe_model.link)
        self.assertFalse(recipe_model.preparation)
        self.assertEqual(recipe_model.author, user)
        self.assertEqual(waiting_model.ingredients.count(), 0)

    def test_push_updates_to_recipe_update_recipe_minimal_data(self):
        user = User(username="test", email="test@test.com")
        recipe_model = Recipe(id=1, title='testold', time=15, difficulty=3, link='http://testold.com',
                              preparation='testold',
                              author=user,
                              ingredients=[RecipeIngredient(title='test1old', amount=21, unit='g'),
                                           RecipeIngredient(title='test2', amount=1, unit='kg')])
        waiting_model = WaitingRecipe(title='test',
                                      author=user, updated_recipe=recipe_model)
        recipe_model = _push_updates_to_recipe(waiting_model)

        self.assertEqual(recipe_model.id, 1)
        self.assertEqual(recipe_model.title, 'test')
        self.assertFalse(recipe_model.time)
        self.assertFalse(recipe_model.difficulty)
        self.assertFalse(recipe_model.link)
        self.assertFalse(recipe_model.preparation)
        self.assertEqual(recipe_model.author, user)
        self.assertEqual(waiting_model.ingredients.count(), 0)

    def test_push_updates_to_recipe_update_recipe_add_ingredient(self):
        user = User(username="test", email="test@test.com")
        recipe_model = Recipe(id=1, title='test', author=user,
                              ingredients=[RecipeIngredient(title='test1', amount=1, unit='kg')])
        waiting_model = WaitingRecipe(title='test',
                                      author=user, ingredients=[RecipeIngredient(title='test1', amount=1, unit='kg'),
                                                                RecipeIngredient(title='test2', amount=1, unit='kg')],
                                      updated_recipe=recipe_model)
        recipe_model = _push_updates_to_recipe(waiting_model)

        self.assertEqual(waiting_model.ingredients.count(), 2)
        self.assertEqual(recipe_model.ingredients[0].title, 'test1')
        self.assertEqual(recipe_model.ingredients[0].amount, 1)
        self.assertEqual(recipe_model.ingredients[0].unit, 'kg')
        self.assertEqual(recipe_model.ingredients[1].title, 'test2')
        self.assertEqual(recipe_model.ingredients[1].amount, 1)
        self.assertEqual(recipe_model.ingredients[1].unit, 'kg')

    def test_push_updates_to_recipe_update_recipe_delete_ingredient(self):
        user = User(username="test", email="test@test.com")
        recipe_model = Recipe(id=1, title='test', author=user,
                              ingredients=[RecipeIngredient(title='test1', amount=1, unit='kg'),
                                           RecipeIngredient(title='test2', amount=1, unit='kg')])
        waiting_model = WaitingRecipe(title='test',
                                      author=user, ingredients=[RecipeIngredient(title='test1', amount=1, unit='kg')],
                                      updated_recipe=recipe_model)
        recipe_model = _push_updates_to_recipe(waiting_model)

        self.assertEqual(waiting_model.ingredients.count(), 1)
        self.assertEqual(recipe_model.ingredients[0].title, 'test1')
        self.assertEqual(recipe_model.ingredients[0].amount, 1)
        self.assertEqual(recipe_model.ingredients[0].unit, 'kg')
