from werkzeug.exceptions import NotFound

from app import db
from app.models import User, RecipeIngredient, Recipe, WaitingRecipe, WaitingRecipeIngredient
from app.services import get_recipes, get_user_recipes, get_waiting_recipes, accept_waiting, get_recipe, \
    get_user_by_name, get_waiting_recipe, save_recipe
from tests.base_test import TestAppSetUp


class TestServices(TestAppSetUp):
    def setUp(self):
        super().setUp()

        # users test test2 admin
        self.user = User(username="test", email="test@test.com")
        self.user.set_password("test")
        db.session.add(self.user)

        self.user2 = User(username="test2", email="test2@test.com")
        self.user2.set_password("test")
        db.session.add(self.user2)

        self.user3 = User(username="test3", email="test3@test.com")
        self.user3.set_password("test")
        db.session.add(self.user3)

        self.admin = User(username="admin", email="admin@test.com")
        self.admin.set_password("admin")
        db.session.add(self.admin)

        self.recipe_model = Recipe(title='test', time=1, difficulty=1, link='http://test.com', preparation='test',
                                   author=self.user, ingredients=[RecipeIngredient(title='test1', amount=1, unit='kg'),
                                                                  RecipeIngredient(title='test2', amount=1, unit='kg')])
        db.session.add(self.recipe_model)

        self.recipe_model_2 = Recipe(title='test2', time=2, difficulty=2, link='http://test2.com', preparation='test',
                                     author=self.user,
                                     ingredients=[RecipeIngredient(title='test1', amount=2, unit='kg'),
                                                  RecipeIngredient(title='test2', amount=2, unit='dag')])
        db.session.add(self.recipe_model_2)

        self.waiting_model = WaitingRecipe(title='test', time=3, difficulty=3, link='http://test3.com',
                                           preparation='test3',
                                           author=self.user2,
                                           updated_recipe=self.recipe_model,
                                           ingredients=[WaitingRecipeIngredient(title='test1', amount=3, unit='g'),
                                                        WaitingRecipeIngredient(title='test2', amount=3, unit='g')])
        db.session.add(self.waiting_model)

        self.waiting_model_2 = WaitingRecipe(title='test2', time=4, difficulty=4, link='http://test4.com',
                                             preparation='test4',
                                             author=self.user3,
                                             ingredients=[WaitingRecipeIngredient(title='test1', amount=3, unit='g'),
                                                          WaitingRecipeIngredient(title='test2', amount=3, unit='g')])
        db.session.add(self.waiting_model_2)

        self.waiting_model_3 = WaitingRecipe(title='test3', time=4, difficulty=4, link='http://test4.com',
                                             preparation='test4',
                                             author=self.user3,
                                             ingredients=[WaitingRecipeIngredient(title='test1', amount=3, unit='g'),
                                                          WaitingRecipeIngredient(title='test2', amount=3, unit='g')])
        db.session.add(self.waiting_model_3)

        db.session.commit()

    def test_get_recipes(self):
        recipes = get_recipes(1, 1000)
        self.assertEqual(len(recipes.items), 2)

    def test_get_user_recipes_two_recipes(self):
        recipes = get_user_recipes(self.user, 1, 1000)
        self.assertEqual(len(recipes.items), 2)

    def test_get_user_recipes_no_recipes(self):
        recipes = get_user_recipes(self.user2, 1, 1000)
        self.assertEqual(len(recipes.items), 0)

    def test_get_waiting_recipes_no_recipes(self):
        waiting_recipes = get_waiting_recipes(self.user, 1, 1000)
        self.assertEqual(len(waiting_recipes.items), 0)

    def test_get_waiting_recipes_two_recipes(self):
        waiting_recipes = get_waiting_recipes(self.user3, 1, 1000)
        self.assertEqual(len(waiting_recipes.items), 2)

    def test_get_waiting_recipes_admin(self):
        waiting_recipes = get_waiting_recipes(self.admin, 1, 1000)
        self.assertEqual(len(waiting_recipes.items), 3)

    def test_accept_waiting_new_recipe(self):
        accept_waiting(self.waiting_model_2)
        self.assertEqual(len(WaitingRecipe.query.all()), 2)
        self.assertEqual(len(Recipe.query.all()), 3)

    def test_accept_waiting_updated_recipe(self):
        accept_waiting(self.waiting_model)
        self.assertEqual(len(WaitingRecipe.query.all()), 2)
        self.assertEqual(len(Recipe.query.all()), 2)

    def test_save_recipe_recipe(self):
        id_ = len(Recipe.query.all()) + 1
        recipe_model = Recipe(title='testtest',
                              ingredients=[RecipeIngredient(title='test1'),
                                           RecipeIngredient(title='test2')])
        save_recipe(recipe_model)
        self.assertEqual(recipe_model.id, id_)

    def test_save_recipe_recipe_with_empty_ingredients(self):
        recipe_model = Recipe(title='testtest',
                              ingredients=[RecipeIngredient(title='test1'),
                                           RecipeIngredient(title=''),
                                           RecipeIngredient(title=None),
                                           RecipeIngredient(title='test2'),
                                           RecipeIngredient(title=None)])
        save_recipe(recipe_model)
        self.assertEqual(recipe_model.ingredients.count(), 2)

    def test_save_recipe_waiting_recipe(self):
        id_ = len(WaitingRecipe.query.all()) + 1
        waiting_model = WaitingRecipe(title='testtest',
                                      ingredients=[WaitingRecipeIngredient(title='test1'),
                                                   WaitingRecipeIngredient(title='test2')])
        save_recipe(waiting_model)
        self.assertEqual(waiting_model.id, id_)

    def test_save_recipe_waiting_recipe_with_empty_ingredients(self):
        waiting_model = WaitingRecipe(title='testtest',
                                      ingredients=[WaitingRecipeIngredient(title='test1'),
                                                   WaitingRecipeIngredient(title=''),
                                                   WaitingRecipeIngredient(title=None),
                                                   WaitingRecipeIngredient(title='test2'),
                                                   WaitingRecipeIngredient(title=None)])
        save_recipe(waiting_model)
        self.assertEqual(waiting_model.ingredients.count(), 2)

    def test_get_recipe_existing_pk(self):
        id_ = self.recipe_model.id
        recipe = get_recipe(id_)
        self.assertEqual(self.recipe_model.__repr__(), recipe.__repr__())

    def test_get_recipe_not_existing_pk(self):
        id_ = len(Recipe.query.all()) + 1
        self.assertRaises(NotFound, get_recipe, id_)

    def test_get_waiting_recipe_existing_pk(self):
        id_ = self.waiting_model.id
        waiting = get_waiting_recipe(id_)
        self.assertEqual(self.waiting_model.__repr__(), waiting.__repr__())

    def test_get_waiting_recipe_not_existing_pk(self):
        id_ = len(WaitingRecipe.query.all()) + 1
        self.assertRaises(NotFound, get_waiting_recipe, id_)

    def test_get_user_by_name_existing(self):
        user = get_user_by_name(self.user.username)
        self.assertEqual(self.user.__repr__(), user.__repr__())

    def test_get_user_by_name_not_existing(self):
        user = get_user_by_name('asdfgh')
        self.assertIsNone(user)
