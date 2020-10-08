from datetime import datetime
from unittest.mock import Mock

import pytest
from werkzeug.exceptions import NotFound

from app import db
from app.models import User, RecipeIngredient, Recipe, WaitingRecipe, WaitingRecipeIngredient
from app.services import get_recipes, get_user_recipes, get_waiting_recipes, accept_waiting, get_recipe, \
    get_user_by_name, get_waiting_recipe, save_recipe, search_recipe, reject_waiting, get_recipe_by_title
from tests.base_test import TestAppSetUp


@pytest.fixture
def ext_users_set(users_set, make_user):
    user1, user2, admin = users_set
    user3 = make_user("test3", "test", "test3@test.com")
    return user1, user2, user3, admin


class TestServices:

    @pytest.fixture
    def recipes_users_set(self, test_client, database, ext_users_set, make_recipe, make_waiting_recipe):
        user1, user2, user3, admin = ext_users_set
        recipe1 = make_recipe(title='test', time=1, difficulty=1, link='http://test.com', preparation='test',
                              author=user1, ingredients=[{'title': 'test1', 'amount': 1, 'unit': 'kg'},
                                                         {'title': 'test2', 'amount': 1, 'unit': 'kg'}])
        recipe2 = make_recipe(title='test2', time=2, difficulty=2, link='http://test2.com', preparation='test',
                              author=user1, ingredients=[{'title': 'test1', 'amount': 2, 'unit': 'kg'},
                                                         {'title': 'test2', 'amount': 2, 'unit': 'dag'}])
        waiting_recipe1 = make_waiting_recipe(title='test', time=3, difficulty=3, link='http://test3.com',
                                              preparation='test', author=user2, updated_recipe=recipe1,
                                              ingredients=[{'title': 'test1', 'amount': 3, 'unit': 'g'},
                                                           {'title': 'test2', 'amount': 3, 'unit': 'g'}])
        waiting_recipe2 = make_waiting_recipe(title='test2', time=4, difficulty=4, link='http://test4.com',
                                              preparation='test4', author=user3, updated_recipe=None,
                                              ingredients=[{'title': 'test1', 'amount': 3, 'unit': 'g'},
                                                           {'title': 'test2', 'amount': 3, 'unit': 'g'}])
        waiting_recipe3 = make_waiting_recipe(title='test3', time=4, difficulty=4, link='http://test4.com',
                                              preparation='test4', author=user3, updated_recipe=None,
                                              ingredients=[{'title': 'test1', 'amount': 3, 'unit': 'g'},
                                                           {'title': 'test2', 'amount': 3, 'unit': 'g'}])
        return user1, user2, user3, admin, recipe1, recipe2, waiting_recipe1, waiting_recipe2, waiting_recipe3

    def test_get_recipes(self, recipes_users_set):
        recipes = get_recipes(1, 1000)
        assert len(recipes.items) == 2

    def test_get_user_recipes_two_recipes(self, recipes_users_set):
        user1, user2, user3, admin, recipe1, recipe2, waiting_recipe1, waiting_recipe2, waiting_recipe3 = recipes_users_set
        recipes = get_user_recipes(user1, 1, 1000)
        assert len(recipes.items) == 2

    def test_get_user_recipes_no_recipes(self, recipes_users_set):
        user1, user2, user3, admin, recipe1, recipe2, waiting_recipe1, waiting_recipe2, waiting_recipe3 = recipes_users_set
        recipes = get_user_recipes(user2, 1, 1000)
        assert len(recipes.items) == 0

    def test_get_waiting_recipes_no_recipes(self, recipes_users_set):
        user1, user2, user3, admin, recipe1, recipe2, waiting_recipe1, waiting_recipe2, waiting_recipe3 = recipes_users_set
        waiting_recipes = get_waiting_recipes(user1, 1, 1000)
        assert 0 == len(waiting_recipes.items)

    def test_get_waiting_recipes_two_recipes(self, recipes_users_set):
        user1, user2, user3, admin, recipe1, recipe2, waiting_recipe1, waiting_recipe2, waiting_recipe3 = recipes_users_set
        waiting_recipes = get_waiting_recipes(user3, 1, 1000)
        assert 2 == len(waiting_recipes.items)

    def test_get_waiting_recipes_admin(self, recipes_users_set):
        user1, user2, user3, admin, recipe1, recipe2, waiting_recipe1, waiting_recipe2, waiting_recipe3 = recipes_users_set
        waiting_recipes = get_waiting_recipes(admin, 1, 1000)
        assert 3 == len(waiting_recipes.items)

    def test_accept_waiting_new_recipe(self, recipes_users_set):
        user1, user2, user3, admin, recipe1, recipe2, waiting_recipe1, waiting_recipe2, waiting_recipe3 = recipes_users_set
        accept_waiting(waiting_recipe2)
        assert len(WaitingRecipe.query.all()) == 2
        assert len(Recipe.query.all()) == 3

    def test_accept_waiting_updated_recipe(self, recipes_users_set):
        user1, user2, user3, admin, recipe1, recipe2, waiting_recipe1, waiting_recipe2, waiting_recipe3 = recipes_users_set
        accept_waiting(waiting_recipe1)
        assert len(WaitingRecipe.query.all()) == 2
        assert len(Recipe.query.all()) == 2

    def test_save_recipe_recipe(self, recipes_users_set):
        id_ = len(Recipe.query.all()) + 1
        recipe_model = Recipe(title='testtest',
                              ingredients=[RecipeIngredient(title='test1'),
                                           RecipeIngredient(title='test2')])
        save_recipe(recipe_model)
        assert recipe_model.id == id_

    def test_save_recipe_recipe_with_empty_ingredients(self, recipes_users_set):
        recipe_model = Recipe(title='testtest',
                              ingredients=[RecipeIngredient(title='test1'),
                                           RecipeIngredient(title=''),
                                           RecipeIngredient(title=None),
                                           RecipeIngredient(title='test2'),
                                           RecipeIngredient(title=None)])
        save_recipe(recipe_model)
        assert recipe_model.ingredients.count() == 2

    def test_save_recipe_waiting_recipe(self, recipes_users_set):
        id_ = len(WaitingRecipe.query.all()) + 1
        waiting_model = WaitingRecipe(title='testtest',
                                      ingredients=[WaitingRecipeIngredient(title='test1'),
                                                   WaitingRecipeIngredient(title='test2')])
        save_recipe(waiting_model)
        assert waiting_model.id == id_

    def test_save_recipe_waiting_recipe_with_empty_ingredients(self, recipes_users_set):
        waiting_model = WaitingRecipe(title='testtest',
                                      ingredients=[WaitingRecipeIngredient(title='test1'),
                                                   WaitingRecipeIngredient(title=''),
                                                   WaitingRecipeIngredient(title=None),
                                                   WaitingRecipeIngredient(title='test2'),
                                                   WaitingRecipeIngredient(title=None)])
        save_recipe(waiting_model)
        assert waiting_model.ingredients.count() == 2

    def test_get_recipe_existing_pk(self, recipes_users_set):
        user1, user2, user3, admin, recipe1, recipe2, waiting_recipe1, waiting_recipe2, waiting_recipe3 = recipes_users_set
        id_ = recipe1.id
        recipe = get_recipe(id_)
        assert recipe1.__repr__(), recipe.__repr__()

    def test_get_recipe_not_existing_pk(self, recipes_users_set):
        id_ = len(Recipe.query.all()) + 1
        with pytest.raises(NotFound):
            get_recipe(id_)

    def test_get_waiting_recipe_existing_pk(self, recipes_users_set):
        user1, user2, user3, admin, recipe1, recipe2, waiting_recipe1, waiting_recipe2, waiting_recipe3 = recipes_users_set
        id_ = waiting_recipe1.id
        waiting = get_waiting_recipe(id_)
        assert waiting_recipe1.__repr__() == waiting.__repr__()

    def test_get_waiting_recipe_not_existing_pk(self, recipes_users_set):
        id_ = len(WaitingRecipe.query.all()) + 1
        with pytest.raises(NotFound):
            get_waiting_recipe(id_)

    def test_get_user_by_name_existing(self, recipes_users_set):
        user1, user2, user3, admin, recipe1, recipe2, waiting_recipe1, waiting_recipe2, waiting_recipe3 = recipes_users_set
        user = get_user_by_name(user1.username)
        assert user1.__repr__() == user.__repr__()

    def test_get_user_by_name_not_existing(self, recipes_users_set):
        user = get_user_by_name('asdfgh')
        assert user is None

    def test_get_recipe_by_title_existing(self, recipes_users_set):
        user1, user2, user3, admin, recipe1, recipe2, waiting_recipe1, waiting_recipe2, waiting_recipe3 = recipes_users_set
        recipe = get_recipe_by_title(recipe1.title)
        assert recipe1.__repr__() == recipe.__repr__()

    def test_get_recipe_by_title_not_existing(self, recipes_users_set):
        recipe = get_recipe_by_title('asdfgh')
        assert recipe is None


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

        self.waiting_model = WaitingRecipe(title='waiting_second', author=self.user2,
                                           create_date=datetime(2019, 1, 20),
                                           last_modified=datetime(2019, 11, 1))
        db.session.add(self.waiting_model)

        self.waiting_model2 = WaitingRecipe(title='waiting_first', author=self.user2,
                                            create_date=datetime(2019, 1, 30),
                                            last_modified=datetime(2019, 10, 1))
        db.session.add(self.waiting_model2)

        self.waiting_model3 = WaitingRecipe(title='waiting_third', author=self.user,
                                            create_date=datetime(2019, 1, 10),
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


class TestServicesSearch:
    def test_search_recipe_convert_strings_to_ints(self, test_client, database, ):
        from app import models
        models.query_index = Mock(return_value=([1], 2))
        search_recipe('test', '1', '1')
        models.query_index.assert_called_once_with('recipe', 'test', 1, 1)


class TestServicesRefusedWaitingRecipe(TestAppSetUp):
    def setUp(self):
        super().setUp()
        # users test admin
        self.user = User(username="test", email="test@test.com")
        self.user.set_password("test")
        db.session.add(self.user)

        self.admin = User(username="admin", email="admin@test.com")
        self.admin.set_password("admin")
        db.session.add(self.admin)

        self.waiting_model_pending = WaitingRecipe(title='waiting_pending', author=self.user, refused=False)
        db.session.add(self.waiting_model_pending)

        self.waiting_model_refused = WaitingRecipe(title='waiting_refused', author=self.user, refused=True)
        db.session.add(self.waiting_model_refused)

        self.recipe_model = Recipe(title='accepted_recipe', author=self.user)

        db.session.commit()

    def test_get_waiting_recipes_returns_only_pending_for_admin(self):
        waiting_list = get_waiting_recipes(self.admin, 1, 100)
        self.assertFalse(any(item.refused for item in waiting_list.items))

    def test_get_waiting_recipes_returns_pending_and_refused_for_user(self):
        waiting_list = get_waiting_recipes(self.user, 1, 100)
        self.assertTrue(any(item.refused for item in waiting_list.items))
        self.assertTrue(any(not item.refused for item in waiting_list.items))

    def test_get_waiting_recipes_returns_refused_status(self):
        waiting_list = get_waiting_recipes(self.user, 1, 100)
        self.assertTrue(all(hasattr(item, 'refused') for item in waiting_list.items))

    def test_save_recipe_sets_pending_to_pending_if_waiting(self):
        save_recipe(self.waiting_model_pending)
        self.assertFalse(self.waiting_model_pending.refused)

    def test_save_recipe_sets_refused_to_pending_if_waiting(self):
        save_recipe(self.waiting_model_refused)
        self.assertFalse(self.waiting_model_refused.refused)

    def test_save_recipe_inits_status_pending_for_waiting(self):
        waiting_model = WaitingRecipe(title='waiting_new', author=self.user)
        save_recipe(waiting_model)
        self.assertFalse(self.waiting_model_pending.refused)

    def test_save_recipe_dont_set_status_pending_for_accepted(self):
        save_recipe(self.recipe_model)
        self.assertFalse(hasattr(self.recipe_model, 'refused'))

    def test_reject_waiting_sets_refused_to_true_when_false(self):
        id_ = self.waiting_model_pending.id
        reject_waiting(self.waiting_model_pending)
        rejected_recipe = WaitingRecipe.query.get_or_404(id_)
        self.assertTrue(rejected_recipe.refused)

    def test_reject_waiting_sets_refused_to_true_when_true(self):
        id_ = self.waiting_model_refused.id
        reject_waiting(self.waiting_model_refused)
        rejected_recipe = WaitingRecipe.query.get_or_404(id_)
        self.assertTrue(rejected_recipe.refused)
