from app.models.recipes import Recipe, RecipeIngredient, StatusEnum


def test_add_ingredient_parameters():
    recipe_model = Recipe(ingredients=[])
    recipe_model.add_ingredient(title='test1', amount=1, unit='kg')

    assert recipe_model.ingredients[0].title == 'test1'
    assert recipe_model.ingredients[0].amount == 1
    assert recipe_model.ingredients[0].unit == 'kg'


def test_add_ingredient_length_no_list():
    recipe_model = Recipe()
    recipe_model.add_ingredient(title='test1', amount=1, unit='kg')

    assert len(recipe_model.ingredients) == 1


def test_add_ingredient_length_empty_list():
    recipe_model = Recipe(ingredients=[])
    recipe_model.add_ingredient(title='test1', amount=1, unit='kg')

    assert len(recipe_model.ingredients) == 1


def test_add_ingredient_length_list_with_two():
    recipe_model = Recipe(ingredients=[RecipeIngredient(), RecipeIngredient()])
    recipe_model.add_ingredient(title='test1', amount=1, unit='kg')

    assert len(recipe_model.ingredients) == 3


def test_add_ingredient_parameters_only_title():
    recipe_model = Recipe(ingredients=[])
    recipe_model.add_ingredient(title='test1')

    assert recipe_model.ingredients[0].title == 'test1'
    assert recipe_model.ingredients[0].amount is None
    assert recipe_model.ingredients[0].unit is None


def test_clear_empty_ingredients_with_empty():
    recipe_model = Recipe(ingredients=[RecipeIngredient(title='test1'), RecipeIngredient(title=''),
                                       RecipeIngredient(title=None), RecipeIngredient(title='test2'),
                                       RecipeIngredient(title=None)])
    recipe_model.clear_empty_ingredients()

    assert len(recipe_model.ingredients) == 2
    assert recipe_model.ingredients[0].title == 'test1'
    assert recipe_model.ingredients[1].title == 'test2'


def test_clear_empty_ingredients_without_empty():
    recipe_model = Recipe(
        ingredients=[RecipeIngredient(title='test1'), RecipeIngredient(title='test2')])
    recipe_model.clear_empty_ingredients()

    assert len(recipe_model.ingredients) == 2
    assert recipe_model.ingredients[0].title == 'test1'
    assert recipe_model.ingredients[1].title == 'test2'


def test_accept_from_pending():
    recipe_model = Recipe(status=StatusEnum.pending)
    recipe_model.accept()
    assert recipe_model.status == StatusEnum.accepted


def test_accept_from_refused():
    recipe_model = Recipe(status=StatusEnum.refused)
    recipe_model.accept()
    assert recipe_model.status == StatusEnum.accepted


def test_reject_from_pending():
    recipe_model = Recipe(status=StatusEnum.pending)
    recipe_model.reject()
    assert recipe_model.status == StatusEnum.refused


def test_reject_from_accepted():
    recipe_model = Recipe(status=StatusEnum.accepted)
    recipe_model.reject()
    assert recipe_model.status == StatusEnum.refused


def test_reset_status_from_accepted():
    recipe_model = Recipe(status=StatusEnum.accepted)
    recipe_model.reset_status()
    assert recipe_model.status == StatusEnum.pending


def test_reset_status_from_refused():
    recipe_model = Recipe(status=StatusEnum.refused)
    recipe_model.reset_status()
    assert recipe_model.status == StatusEnum.pending


def test_default_status_is_pending(test_client, make_recipe):
    recipe_model = make_recipe(title='test')
    assert recipe_model.status == StatusEnum.pending
