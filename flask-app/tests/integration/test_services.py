from app import db
from app.models import User, RecipeIngredient, Recipe, WaitingRecipe, WaitingRecipeIngredient
from app.services import get_recipes, get_user_recipes, get_waiting_recipes
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

        recipe_model = Recipe(title='test', time=1, difficulty=1, link='http://test.com', preparation='test',
                              author=self.user, ingredients=[RecipeIngredient(title='test1', amount=1, unit='kg'),
                                                             RecipeIngredient(title='test2', amount=1, unit='kg')])
        db.session.add(recipe_model)

        recipe_model_2 = Recipe(title='test2', time=2, difficulty=2, link='http://test2.com', preparation='test',
                                author=self.user, ingredients=[RecipeIngredient(title='test1', amount=2, unit='kg'),
                                                               RecipeIngredient(title='test2', amount=2, unit='dag')])
        db.session.add(recipe_model_2)

        waiting_model = WaitingRecipe(title='test', time=3, difficulty=3, link='http://test3.com', preparation='test3',
                                      author=self.user2,
                                      ingredients=[WaitingRecipeIngredient(title='test1', amount=3, unit='g'),
                                                   WaitingRecipeIngredient(title='test2', amount=3, unit='g')])
        db.session.add(waiting_model)

        waiting_model_2 = WaitingRecipe(title='test2', time=4, difficulty=4, link='http://test4.com',
                                        preparation='test4',
                                        author=self.user3,
                                        ingredients=[WaitingRecipeIngredient(title='test1', amount=3, unit='g'),
                                                     WaitingRecipeIngredient(title='test2', amount=3, unit='g')])
        db.session.add(waiting_model_2)

        waiting_model_3 = WaitingRecipe(title='test3', time=4, difficulty=4, link='http://test4.com',
                                        preparation='test4',
                                        author=self.user3,
                                        ingredients=[WaitingRecipeIngredient(title='test1', amount=3, unit='g'),
                                                     WaitingRecipeIngredient(title='test2', amount=3, unit='g')])
        db.session.add(waiting_model_3)

        db.session.commit()

    def test_get_all_recpies(self):
        recipes = get_recipes(1, 1000)
        self.assertEqual(len(recipes.items), 2)

    def test_get_user_recipes_two_recipes(self):
        recipes = get_user_recipes(self.user, 1, 1000)
        self.assertEqual(len(recipes.items), 2)

    def test_get_user_recipes_no_recipes(self):
        recipes = get_user_recipes(self.user2, 1, 1000)
        self.assertEqual(len(recipes.items), 0)

    def test_get_all_waiting_recipes_no_recipes(self):
        waiting_recipes = get_waiting_recipes(self.user, 1, 1000)
        self.assertEqual(len(waiting_recipes.items), 0)

    def test_get_all_waiting_recipes_two_recipes(self):
        waiting_recipes = get_waiting_recipes(self.user3, 1, 1000)
        self.assertEqual(len(waiting_recipes.items), 2)

    def test_get_all_waiting_recipes_admin(self):
        waiting_recipes = get_waiting_recipes(self.admin, 1, 1000)
        self.assertEqual(len(waiting_recipes.items), 3)
