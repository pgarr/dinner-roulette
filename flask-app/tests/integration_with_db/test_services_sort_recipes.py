from datetime import datetime

from app import db
from app.models import User, Recipe, WaitingRecipe
from app.services import get_recipes, get_user_recipes, get_waiting_recipes
from tests.base_test import TestAppSetUp


class TestServicesSortBasic(TestAppSetUp):
    def setUp(self):
        super().setUp()
        # users test test2 test3 admin
        self.user = User(username="test", email="test@test.com")
        self.user.set_password("test")
        db.session.add(self.user)

        self.user2 = User(username="test2", email="test2@test.com")
        self.user2.set_password("test")
        db.session.add(self.user2)

        self.admin = User(username="admin", email="admin@test.com")
        self.admin.set_password("admin")
        db.session.add(self.admin)

        self.recipe_model = Recipe(title='third', author=self.user2, create_date=datetime(2019, 1, 10),
                                   last_modified=datetime(2019, 12, 1))
        db.session.add(self.recipe_model)

        self.recipe_model2 = Recipe(title='first', author=self.user, create_date=datetime(2019, 1, 30),
                                    last_modified=datetime(2019, 11, 1))
        db.session.add(self.recipe_model2)

        self.recipe_model3 = Recipe(title='second', author=self.user2, create_date=datetime(2019, 1, 20),
                                    last_modified=datetime(2019, 6, 1))
        db.session.add(self.recipe_model3)

        self.waiting_model = WaitingRecipe(title='waiting_second', author=self.user2, create_date=datetime(2019, 1, 20),
                                           last_modified=datetime(2019, 11, 1))
        db.session.add(self.waiting_model)

        self.waiting_model2 = WaitingRecipe(title='waiting_first', author=self.user2, create_date=datetime(2019, 1, 30),
                                            last_modified=datetime(2019, 10, 1))
        db.session.add(self.waiting_model2)

        self.waiting_model3 = WaitingRecipe(title='waiting_third', author=self.user, create_date=datetime(2019, 1, 10),
                                            last_modified=datetime(2019, 12, 1))
        db.session.add(self.waiting_model3)

        db.session.commit()

    def test_recipes_sort_by_create_date_from_latest(self):
        recipes = get_recipes(1, 100)
        self.assertEqual(3, len(recipes.items))
        self.assertEqual('first', recipes.items[0].title)
        self.assertEqual('second', recipes.items[1].title)
        self.assertEqual('third', recipes.items[2].title)

    def test_my_recipes_sort_by_create_date_from_latest(self):
        recipes = get_user_recipes(self.user2, 1, 100)
        self.assertEqual(2, len(recipes.items))
        self.assertEqual('second', recipes.items[0].title)
        self.assertEqual('third', recipes.items[1].title)

    def test_waiting_recipes_user_sort_by_last_update_from_oldest(self):
        recipes = get_waiting_recipes(self.user2, 1, 100)
        self.assertEqual(2, len(recipes.items))
        self.assertEqual('waiting_first', recipes.items[0].title)
        self.assertEqual('waiting_second', recipes.items[1].title)

    def test_waiting_recipes_admin_sort_by_last_update_from_oldest(self):
        recipes = get_waiting_recipes(self.admin, 1, 100)
        self.assertEqual(3, len(recipes.items))
        self.assertEqual('waiting_first', recipes.items[0].title)
        self.assertEqual('waiting_second', recipes.items[1].title)
        self.assertEqual('waiting_third', recipes.items[2].title)
