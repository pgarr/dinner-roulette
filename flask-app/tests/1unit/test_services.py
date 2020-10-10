import pytest

from app.models import Recipe, User, WaitingRecipe, RecipeIngredient, WaitingRecipeIngredient
from app.services import clone_recipe_to_waiting, init_waiting_recipe, _push_updates_to_recipe


@pytest.fixture
def user():
    return User(username="test", email="test@test.com")


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
