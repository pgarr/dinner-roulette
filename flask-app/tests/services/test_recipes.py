from datetime import datetime

import pytest
from werkzeug.exceptions import NotFound

from app.models.auth import User
from app.models.recipes import Recipe, WaitingRecipe, RecipeIngredient, WaitingRecipeIngredient
from app.services.recipes import clone_recipe_to_waiting, init_waiting_recipe, _push_updates_to_recipe, \
    get_user_waiting_recipes, save_recipe, reject_waiting, get_waiting_recipes, get_recipes, get_user_recipes, \
    accept_waiting, get_recipe, get_waiting_recipe, get_recipe_by_title, get_all_pending_waiting_recipes


@pytest.fixture
def user():
    return User(username="test", email="test@test.com")


@pytest.fixture
def ext_users_set(users_set, make_user):
    user1, user2, admin = users_set
    user3 = make_user("test3", "test", "test3@test.com")
    return user1, user2, user3, admin


def test_clone_recipe_to_waiting_empty():
    recipe_model = Recipe()
    waiting_model = clone_recipe_to_waiting(recipe_model)

    assert isinstance(waiting_model, WaitingRecipe)
    assert not waiting_model.title
    assert not waiting_model.time
    assert not waiting_model.difficulty
    assert not waiting_model.link
    assert not waiting_model.preparation
    assert not waiting_model.author
    assert waiting_model.ingredients.count() == 0


def test_clone_recipe_to_waiting_full(user):
    recipe_model = Recipe(title='test', time=1, difficulty=1, link='http://test.com', preparation='test', author=user,
                          ingredients=[RecipeIngredient(title='test1', amount=1, unit='kg'),
                                       RecipeIngredient(title='test2', amount=1, unit='kg')])
    waiting_model = clone_recipe_to_waiting(recipe_model)

    assert waiting_model.title == 'test'
    assert waiting_model.time == 1
    assert waiting_model.difficulty == 1
    assert waiting_model.link == 'http://test.com'
    assert waiting_model.preparation == 'test'
    assert waiting_model.author == user
    assert waiting_model.ingredients.count() == 2
    assert isinstance(waiting_model.ingredients[0], WaitingRecipeIngredient)
    assert waiting_model.ingredients[0].title == 'test1'
    assert waiting_model.ingredients[0].amount == 1
    assert waiting_model.ingredients[0].unit == 'kg'
    assert isinstance(waiting_model.ingredients[1], WaitingRecipeIngredient)
    assert waiting_model.ingredients[1].title == 'test2'
    assert waiting_model.ingredients[1].amount == 1
    assert waiting_model.ingredients[1].unit == 'kg'


def test_init_waiting_recipe_all_data(user):
    waiting_model = init_waiting_recipe(title='test', time=1, difficulty=1, link='http://test.com', preparation='test',
                                        author=user)

    assert waiting_model.title == 'test'
    assert waiting_model.time == 1
    assert waiting_model.difficulty == 1
    assert waiting_model.link == 'http://test.com'
    assert waiting_model.preparation == 'test'
    assert waiting_model.author == user
    assert waiting_model.ingredients.count() == 0


def test_init_waiting_recipe_empty_data():
    waiting_model = init_waiting_recipe()

    assert isinstance(waiting_model, WaitingRecipe)
    assert not waiting_model.title
    assert not waiting_model.time
    assert not waiting_model.difficulty
    assert not waiting_model.link
    assert not waiting_model.preparation
    assert not waiting_model.author
    assert waiting_model.ingredients.count() == 0


def test_push_updates_to_recipe_new_recipe_full_data(user):
    waiting_model = WaitingRecipe(title='test', time=1, difficulty=1, link='http://test.com', preparation='test',
                                  author=user,
                                  ingredients=[WaitingRecipeIngredient(title='test1', amount=1, unit='kg'),
                                               WaitingRecipeIngredient(title='test2', amount=1, unit='kg')])
    recipe_model = _push_updates_to_recipe(waiting_model)

    assert isinstance(recipe_model, Recipe)
    assert not recipe_model.id
    assert recipe_model.title == 'test'
    assert recipe_model.time == 1
    assert recipe_model.difficulty == 1
    assert recipe_model.link == 'http://test.com'
    assert recipe_model.preparation == 'test'
    assert recipe_model.author == user
    assert recipe_model.ingredients.count() == 2
    assert isinstance(recipe_model.ingredients[0], RecipeIngredient)
    assert recipe_model.ingredients[0].title == 'test1'
    assert recipe_model.ingredients[0].amount == 1
    assert recipe_model.ingredients[0].unit == 'kg'
    assert isinstance(recipe_model.ingredients[1], RecipeIngredient)
    assert recipe_model.ingredients[1].title == 'test2'
    assert recipe_model.ingredients[1].amount == 1
    assert recipe_model.ingredients[1].unit == 'kg'


def test_push_updates_to_recipe_update_recipe_full_data(user):
    recipe_model = Recipe(id=1, title='testold', time=15, difficulty=3, link='http://testold.com',
                          preparation='testold', author=user,
                          ingredients=[RecipeIngredient(title='test1old', amount=21, unit='g'),
                                       RecipeIngredient(title='test2', amount=1, unit='kg')])
    waiting_model = WaitingRecipe(title='test', time=1, difficulty=1, link='http://test.com', preparation='test',
                                  author=user,
                                  ingredients=[WaitingRecipeIngredient(title='test1', amount=1, unit='kg'),
                                               WaitingRecipeIngredient(title='test2', amount=1, unit='kg')],
                                  updated_recipe=recipe_model)
    recipe_model = _push_updates_to_recipe(waiting_model)

    assert recipe_model.id == 1
    assert recipe_model.title == 'test'
    assert recipe_model.time == 1
    assert recipe_model.difficulty == 1
    assert recipe_model.link == 'http://test.com'
    assert recipe_model.preparation == 'test'
    assert recipe_model.author == user
    assert recipe_model.ingredients.count() == 2
    assert isinstance(recipe_model.ingredients[0], RecipeIngredient)
    assert recipe_model.ingredients[0].title == 'test1'
    assert recipe_model.ingredients[0].amount == 1
    assert recipe_model.ingredients[0].unit == 'kg'
    assert isinstance(recipe_model.ingredients[1], RecipeIngredient)
    assert recipe_model.ingredients[1].title == 'test2'
    assert recipe_model.ingredients[1].amount == 1
    assert recipe_model.ingredients[1].unit == 'kg'


def test_push_updates_to_recipe_new_recipe_minimal_data(user):
    waiting_model = WaitingRecipe(title='test', author=user)
    recipe_model = _push_updates_to_recipe(waiting_model)

    assert not recipe_model.id
    assert recipe_model.title == 'test'
    assert not recipe_model.time
    assert not recipe_model.difficulty
    assert not recipe_model.link
    assert not recipe_model.preparation
    assert recipe_model.author == user
    assert waiting_model.ingredients.count() == 0


def test_push_updates_to_recipe_update_recipe_minimal_data(user):
    recipe_model = Recipe(id=1, title='testold', time=15, difficulty=3, link='http://testold.com',
                          preparation='testold', author=user,
                          ingredients=[RecipeIngredient(title='test1old', amount=21, unit='g'),
                                       RecipeIngredient(title='test2', amount=1, unit='kg')])
    waiting_model = WaitingRecipe(title='test', author=user, updated_recipe=recipe_model)
    recipe_model = _push_updates_to_recipe(waiting_model)

    assert recipe_model.id == 1
    assert recipe_model.title == 'test'
    assert not recipe_model.time
    assert not recipe_model.difficulty
    assert not recipe_model.link
    assert not recipe_model.preparation
    assert recipe_model.author == user
    assert waiting_model.ingredients.count() == 0


def test_push_updates_to_recipe_update_recipe_add_ingredient(user):
    recipe_model = Recipe(id=1, title='test', author=user,
                          ingredients=[RecipeIngredient(title='test1', amount=1, unit='kg')])
    waiting_model = WaitingRecipe(title='test', author=user,
                                  ingredients=[RecipeIngredient(title='test1', amount=1, unit='kg'),
                                               RecipeIngredient(title='test2', amount=1, unit='kg')],
                                  updated_recipe=recipe_model)
    recipe_model = _push_updates_to_recipe(waiting_model)

    assert waiting_model.ingredients.count() == 2
    assert isinstance(recipe_model.ingredients[0], RecipeIngredient)
    assert recipe_model.ingredients[0].title == 'test1'
    assert recipe_model.ingredients[0].amount == 1
    assert recipe_model.ingredients[0].unit == 'kg'
    assert isinstance(recipe_model.ingredients[1], RecipeIngredient)
    assert recipe_model.ingredients[1].title == 'test2'
    assert recipe_model.ingredients[1].amount == 1
    assert recipe_model.ingredients[1].unit == 'kg'


def test_push_updates_to_recipe_update_recipe_delete_ingredient(user):
    recipe_model = Recipe(id=1, title='test', author=user,
                          ingredients=[RecipeIngredient(title='test1', amount=1, unit='kg'),
                                       RecipeIngredient(title='test2', amount=1, unit='kg')])
    waiting_model = WaitingRecipe(title='test', author=user,
                                  ingredients=[RecipeIngredient(title='test1', amount=1, unit='kg')],
                                  updated_recipe=recipe_model)
    recipe_model = _push_updates_to_recipe(waiting_model)

    assert waiting_model.ingredients.count() == 1
    assert isinstance(recipe_model.ingredients[0], RecipeIngredient)
    assert recipe_model.ingredients[0].title == 'test1'
    assert recipe_model.ingredients[0].amount == 1
    assert recipe_model.ingredients[0].unit == 'kg'


class TestRecipes:

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

    def test_get_user_waiting_recipes_no_recipes(self, recipes_users_set):
        user1, user2, user3, admin, recipe1, recipe2, waiting_recipe1, waiting_recipe2, waiting_recipe3 = recipes_users_set
        waiting_recipes = get_user_waiting_recipes(user1, 1, 1000)
        assert 0 == len(waiting_recipes.items)

    def test_get_user_waiting_recipes_two_recipes(self, recipes_users_set):
        user1, user2, user3, admin, recipe1, recipe2, waiting_recipe1, waiting_recipe2, waiting_recipe3 = recipes_users_set
        waiting_recipes = get_user_waiting_recipes(user3, 1, 1000)
        assert 2 == len(waiting_recipes.items)

    def test_get_all_pending_waiting_recipes(self, recipes_users_set):
        # user1, user2, user3, admin, recipe1, recipe2, waiting_recipe1, waiting_recipe2, waiting_recipe3 = recipes_users_set
        waiting_recipes = get_all_pending_waiting_recipes(1, 1000)
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

    def test_get_recipe_by_title_existing(self, recipes_users_set):
        user1, user2, user3, admin, recipe1, recipe2, waiting_recipe1, waiting_recipe2, waiting_recipe3 = recipes_users_set
        recipe = get_recipe_by_title(recipe1.title)
        assert recipe1.__repr__() == recipe.__repr__()

    def test_get_recipe_by_title_not_existing(self, recipes_users_set):
        recipe = get_recipe_by_title('asdfgh')
        assert recipe is None


class TestSort:

    @pytest.fixture
    def recipes_users_set(self, test_client, database, users_set, make_recipe, make_waiting_recipe):
        user1, user2, admin = users_set
        recipe1 = make_recipe(title='third', author=user2, create_date=datetime(2019, 1, 10),
                              last_modified=datetime(2019, 12, 1))
        recipe2 = make_recipe(title='first', author=user1, create_date=datetime(2019, 1, 30),
                              last_modified=datetime(2019, 11, 1))
        recipe3 = make_recipe(title='second', author=user2, create_date=datetime(2019, 1, 20),
                              last_modified=datetime(2019, 6, 1))
        waiting_recipe1 = make_waiting_recipe(title='waiting_second', author=user2, create_date=datetime(2019, 1, 20),
                                              last_modified=datetime(2019, 11, 1))
        waiting_recipe2 = make_waiting_recipe(title='waiting_first', author=user2, create_date=datetime(2019, 1, 30),
                                              last_modified=datetime(2019, 10, 1))
        waiting_recipe3 = make_waiting_recipe(title='waiting_third', author=user1, create_date=datetime(2019, 1, 10),
                                              last_modified=datetime(2019, 12, 1))
        return user1, user2, admin, recipe1, recipe2, recipe3, waiting_recipe1, waiting_recipe2, waiting_recipe3

    def test_get_recipes_sort_by_create_date_from_latest(self, recipes_users_set):
        recipes = get_recipes(1, 100)
        assert 3 == len(recipes.items)
        assert 'first' == recipes.items[0].title
        assert 'second' == recipes.items[1].title
        assert 'third' == recipes.items[2].title

    def test_get_user_recipes_sort_by_create_date_from_latest(self, recipes_users_set):
        user1, user2, admin, recipe1, recipe2, recipe3, waiting_recipe1, waiting_recipe2, waiting_recipe3 = recipes_users_set
        recipes = get_user_recipes(user2, 1, 100)
        assert 2 == len(recipes.items)
        assert 'second' == recipes.items[0].title
        assert 'third' == recipes.items[1].title

    def test_get_user_waiting_recipes_sort_by_last_update_from_oldest(self, recipes_users_set):
        user1, user2, admin, recipe1, recipe2, recipe3, waiting_recipe1, waiting_recipe2, waiting_recipe3 = recipes_users_set
        recipes = get_user_waiting_recipes(user2, 1, 100)
        assert 2 == len(recipes.items)
        assert 'waiting_first' == recipes.items[0].title
        assert 'waiting_second' == recipes.items[1].title

    def test_get_all_pending_waiting_recipes_sort_by_last_update_from_oldest(self, recipes_users_set):
        # user1, user2, admin, recipe1, recipe2, recipe3, waiting_recipe1, waiting_recipe2, waiting_recipe3 = recipes_users_set
        recipes = get_all_pending_waiting_recipes(1, 100)
        assert 3, len(recipes.items)
        assert 'waiting_first' == recipes.items[0].title
        assert 'waiting_second' == recipes.items[1].title
        assert 'waiting_third' == recipes.items[2].title


class TestRefusedWaitingRecipe:

    @pytest.fixture
    def recipes_users_set(self, test_client, database, users_set, make_recipe, make_waiting_recipe):
        user1, user2, admin = users_set
        recipe1 = make_recipe(title='accepted_recipe', author=user1)
        waiting_recipe1 = make_waiting_recipe(title='waiting_pending', author=user1, refused=False)
        waiting_recipe2 = make_waiting_recipe(title='waiting_refused', author=user1, refused=True)
        return user1, admin, recipe1, waiting_recipe1, waiting_recipe2

    def test_get_all_pending_waiting_recipes_returns_only_pending(self, recipes_users_set):
        # user1, admin, recipe1, waiting_recipe1, waiting_recipe2 = recipes_users_set
        waiting_list = get_all_pending_waiting_recipes(1, 100)
        assert not any(item.refused for item in waiting_list.items)

    def test_get_user_waiting_recipes_returns_pending_and_refused(self, recipes_users_set):
        user1, admin, recipe1, waiting_recipe1, waiting_recipe2 = recipes_users_set
        waiting_list = get_user_waiting_recipes(user1, 1, 100)
        assert any(item.refused for item in waiting_list.items)
        assert any(not item.refused for item in waiting_list.items)

    def test_get_user_waiting_recipes_returns_refused_status(self, recipes_users_set):
        user1, admin, recipe1, waiting_recipe1, waiting_recipe2 = recipes_users_set
        waiting_list = get_user_waiting_recipes(user1, 1, 100)
        assert all(hasattr(item, 'refused') for item in waiting_list.items)

    def test_save_recipe_sets_pending_to_pending_if_waiting(self, recipes_users_set):
        user1, admin, recipe1, waiting_recipe1, waiting_recipe2 = recipes_users_set
        save_recipe(waiting_recipe1)
        assert not waiting_recipe1.refused

    def test_save_recipe_sets_refused_to_pending_if_waiting(self, recipes_users_set):
        user1, admin, recipe1, waiting_recipe1, waiting_recipe2 = recipes_users_set
        save_recipe(waiting_recipe2)
        assert not waiting_recipe2.refused

    def test_save_recipe_inits_status_pending_for_waiting(self, recipes_users_set):
        user1, admin, recipe1, waiting_recipe1, waiting_recipe2 = recipes_users_set
        waiting_model = WaitingRecipe(title='waiting_new', author=user1)
        save_recipe(waiting_model)
        assert not waiting_model.refused

    def test_save_recipe_dont_set_status_pending_for_accepted(self, recipes_users_set):
        user1, admin, recipe1, waiting_recipe1, waiting_recipe2 = recipes_users_set
        save_recipe(recipe1)
        assert not hasattr(recipe1, 'refused')

    def test_reject_waiting_sets_refused_to_true_when_false(self, recipes_users_set):
        user1, admin, recipe1, waiting_recipe1, waiting_recipe2 = recipes_users_set
        id_ = waiting_recipe1.id
        reject_waiting(waiting_recipe1)
        rejected_recipe = WaitingRecipe.query.get_or_404(id_)
        assert rejected_recipe.refused

    def test_reject_waiting_sets_refused_to_true_when_true(self, recipes_users_set):
        user1, admin, recipe1, waiting_recipe1, waiting_recipe2 = recipes_users_set
        id_ = waiting_recipe2.id
        reject_waiting(waiting_recipe2)
        rejected_recipe = WaitingRecipe.query.get_or_404(id_)
        assert rejected_recipe.refused
