from datetime import datetime

import pytest
from werkzeug.exceptions import NotFound

from app.models.recipes import Recipe, RecipeIngredient, StatusEnum
from app.services.recipes import init_recipe, save_recipe, get_recipe, get_accepted_recipes, get_user_recipes, \
    get_pending_recipes, get_recipe_by_title, get_full_all_recipes


class TestRecipesBasic:

    @pytest.fixture
    def recipes_users_set(self, test_client, ext_users_set, make_recipe):
        user1, user2, user3, admin = ext_users_set
        pending_recipe1 = make_recipe(title='test', time=1, difficulty=1, link='http://test.com', preparation='test',
                                      author=user1, status=StatusEnum.pending,
                                      ingredients=[{'title': 'test1', 'amount': 1, 'unit': 'kg'},
                                                   {'title': 'test2', 'amount': 1, 'unit': 'kg'}])
        pending_recipe2 = make_recipe(title='test2', time=2, difficulty=2, link='http://test2.com', preparation='test',
                                      author=user2, status=StatusEnum.pending,
                                      ingredients=[{'title': 'test1', 'amount': 2, 'unit': 'kg'},
                                                   {'title': 'test2', 'amount': 2, 'unit': 'dag'}])
        accepted_recipe1 = make_recipe(title='test', time=1, difficulty=1, link='http://test.com', preparation='test',
                                       author=user1, status=StatusEnum.accepted,
                                       ingredients=[{'title': 'test1', 'amount': 1, 'unit': 'kg'},
                                                    {'title': 'test2', 'amount': 1, 'unit': 'kg'}])
        accepted_recipe2 = make_recipe(title='test2', time=2, difficulty=2, link='http://test2.com', preparation='test',
                                       author=user2, status=StatusEnum.accepted,
                                       ingredients=[{'title': 'test1', 'amount': 2, 'unit': 'kg'},
                                                    {'title': 'test2', 'amount': 2, 'unit': 'dag'}])
        rejected_recipe1 = make_recipe(title='test', time=1, difficulty=1, link='http://test.com', preparation='test',
                                       author=user1, status=StatusEnum.refused,
                                       ingredients=[{'title': 'test1', 'amount': 1, 'unit': 'kg'},
                                                    {'title': 'test2', 'amount': 1, 'unit': 'kg'}])
        rejected_recipe2 = make_recipe(title='test2', time=2, difficulty=2, link='http://test2.com', preparation='test',
                                       author=user2, status=StatusEnum.refused,
                                       ingredients=[{'title': 'test1', 'amount': 2, 'unit': 'kg'},
                                                    {'title': 'test2', 'amount': 2, 'unit': 'dag'}])

        return user1, user2, user3, admin, pending_recipe1, pending_recipe2, accepted_recipe1, accepted_recipe2, rejected_recipe1, rejected_recipe2

    def test_init_recipe_save_author(self, recipes_users_set):
        user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

        model = init_recipe(user1)

        assert model.author == user1

    def test_accept_recipe_refused(self, recipes_users_set):
        user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

        rejected1.accept()

        assert rejected1.status == StatusEnum.accepted

    def test_accept_recipe_pending(self, recipes_users_set):
        user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

        pending1.accept()

        assert pending1.status == StatusEnum.accepted

    def test_accept_recipe_accepted(self, recipes_users_set):
        user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

        accepted1.accept()

        assert accepted1.status == StatusEnum.accepted

    def test_save_recipe_reset_status(self, recipes_users_set):
        user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

        save_recipe(rejected1)

        assert rejected1.status == StatusEnum.pending

    def test_save_recipe_data_ok(self, recipes_users_set):
        user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

        title = 'test'
        time = 2
        difficulty = 3
        link = 'testhttp'
        preparation = 'preparation'
        ingredients = [RecipeIngredient(title='test')]

        recipe = Recipe(title=title, time=time, difficulty=difficulty, link=link, preparation=preparation,
                        ingredients=ingredients, author=user1)

        save_recipe(recipe)

        saved_recipe = Recipe.query.get(recipe.id)

        assert saved_recipe.title == title
        assert saved_recipe.time == time
        assert saved_recipe.link == link
        assert saved_recipe.preparation == preparation
        assert saved_recipe.ingredients[0].title == ingredients[0].title
        assert saved_recipe.author == user1

    def test_save_recipe_clear_empty_ingredients(self, recipes_users_set):
        user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

        recipe = Recipe(title='test', author=user1)
        recipe.ingredients = [RecipeIngredient(title='test'), RecipeIngredient(), RecipeIngredient(),
                              RecipeIngredient(title='test')]
        model = save_recipe(recipe)
        assert len(model.ingredients) == 2

    def test_get_recipe_existing_pk(self, recipes_users_set):
        user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set
        id_ = pending1.id
        recipe = get_recipe(id_)
        assert pending1.__repr__(), recipe.__repr__()

    def test_get_recipe_not_existing_pk(self, recipes_users_set):
        id_ = len(Recipe.query.all()) + 1
        with pytest.raises(NotFound):
            get_recipe(id_)

    def test_get_accepted_recipes(self, recipes_users_set):
        recipes = get_accepted_recipes(1, 1000)
        assert len(recipes.items) == 2

    def test_get_accepted_recipes_when_page_is_str(self, recipes_users_set):
        recipes = get_accepted_recipes('1', '1000')
        assert len(recipes.items) == 2

    def test_get_user_recipes_three_recipes(self, recipes_users_set):
        user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set
        recipes = get_user_recipes(user1, 1, 1000)
        assert len(recipes.items) == 3

    def test_get_user_recipes_three_recipes_when_page_is_str(self, recipes_users_set):
        user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set
        recipes = get_user_recipes(user1, '1', '1000')
        assert len(recipes.items) == 3

    def test_get_user_recipes_no_recipes(self, recipes_users_set):
        user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set
        recipes = get_user_recipes(user3, 1, 1000)
        assert len(recipes.items) == 0

    def test_get_user_recipes_returns_status(self, recipes_users_set):
        user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set
        recipes = get_user_recipes(user1, 1, 1000)
        assert all(hasattr(item, 'status') for item in recipes.items)

    def test_get_pending_recipes(self, recipes_users_set):
        recipes = get_pending_recipes(1, 1000)
        assert len(recipes.items) == 2

    def test_get_pending_recipes_when_page_is_str(self, recipes_users_set):
        recipes = get_pending_recipes('1', '1000')
        assert len(recipes.items) == 2

    @pytest.mark.xfail
    def test_get_recipes(self, recipes_users_set):
        assert False  # TODO when developed

    def test_get_recipe_by_title_existing(self, recipes_users_set):
        user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set
        recipe = get_recipe_by_title(pending1.title)
        assert pending1.__repr__() == recipe.__repr__()

    def test_get_recipe_by_title_not_existing(self, recipes_users_set):
        recipe = get_recipe_by_title('asdfgh')
        assert recipe is None

    def test_reject_recipe_refused(self, recipes_users_set):
        user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

        rejected1.reject()

        assert rejected1.status == StatusEnum.refused

    def test_reject_recipe_pending(self, recipes_users_set):
        user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

        pending1.reject()

        assert pending1.status == StatusEnum.refused

    def test_reject_recipe_accepted(self, recipes_users_set):
        user1, user2, user3, admin, pending1, pending2, accepted1, accepted2, rejected1, rejected2 = recipes_users_set

        accepted1.reject()

        assert accepted1.status == StatusEnum.refused

    def test_get_full_all_recipes_returns_full_data(self, recipes_users_set):
        recipes = get_full_all_recipes()
        assert 6 == len(recipes)

        assert all(hasattr(item, 'id') for item in recipes)
        assert all(hasattr(item, 'title') for item in recipes)
        assert all(hasattr(item, 'time') for item in recipes)
        assert all(hasattr(item, 'difficulty') for item in recipes)
        assert all(hasattr(item, 'link') for item in recipes)
        assert all(hasattr(item, 'preparation') for item in recipes)
        assert all(hasattr(item, 'author') for item in recipes)
        assert all(hasattr(item, 'status') for item in recipes)
        assert all(hasattr(item, 'ingredients') for item in recipes)

        assert all(all(hasattr(ingredient, 'id') for ingredient in item.ingredients) for item in recipes)
        assert all(all(hasattr(ingredient, 'title') for ingredient in item.ingredients) for item in recipes)
        assert all(all(hasattr(ingredient, 'amount') for ingredient in item.ingredients) for item in recipes)
        assert all(all(hasattr(ingredient, 'unit') for ingredient in item.ingredients) for item in recipes)


class TestSort:

    @pytest.fixture
    def recipes_users_set(self, test_client, database, users_set, make_recipe):
        user1, user2, admin = users_set
        accepted1 = make_recipe(title='third', author=user2, create_date=datetime(2019, 1, 10),
                                last_modified=datetime(2019, 12, 1), status=StatusEnum.accepted)
        accepted2 = make_recipe(title='first', author=user1, create_date=datetime(2019, 1, 29),
                                last_modified=datetime(2019, 11, 1), status=StatusEnum.accepted)
        accepted3 = make_recipe(title='second', author=user2, create_date=datetime(2019, 1, 20),
                                last_modified=datetime(2019, 6, 1), status=StatusEnum.accepted)
        pending1 = make_recipe(title='third', author=user2, create_date=datetime(2019, 1, 10),
                               last_modified=datetime(2019, 12, 1), status=StatusEnum.pending)
        pending2 = make_recipe(title='second', author=user1, create_date=datetime(2019, 1, 30),
                               last_modified=datetime(2019, 11, 1), status=StatusEnum.pending)
        pending3 = make_recipe(title='first', author=user2, create_date=datetime(2019, 1, 20),
                               last_modified=datetime(2019, 6, 1), status=StatusEnum.pending)

        return user1, user2, admin, accepted1, accepted2, accepted3, pending1, pending2, pending3

    def test_get_accepted_recipes_sort_by_create_date_from_latest(self, recipes_users_set):
        recipes = get_accepted_recipes(1, 100)
        assert 3 == len(recipes.items)

        assert 'first' == recipes.items[0].title
        assert 'second' == recipes.items[1].title
        assert 'third' == recipes.items[2].title

    def test_get_user_recipes_sort_by_create_date_from_latest(self, recipes_users_set):
        user1, user2, admin, accepted1, accepted2, accepted3, pending1, pending2, pending3 = recipes_users_set
        recipes = get_user_recipes(user1, 1, 100)
        assert 2 == len(recipes.items)

        assert 'second' == recipes.items[0].title
        assert 'first' == recipes.items[1].title

    def test_get_pending_recipes_sort_by_last_update_from_oldest(self, recipes_users_set):
        recipes = get_pending_recipes(1, 100)
        assert 3 == len(recipes.items)

        assert 'first' == recipes.items[0].title
        assert 'second' == recipes.items[1].title
        assert 'third' == recipes.items[2].title
