from app.models.recipes import Recipe, RecipeIngredient, WaitingRecipe, WaitingRecipeIngredient


class AbstractRecipeTests(object):
    recipe_cls = None
    ingredient_cls = None

    def test_add_ingredient_class(self):
        recipe_model = self.recipe_cls(ingredients=[])
        recipe_model.add_ingredient(title='test1', amount=1, unit='kg')
        assert isinstance(recipe_model.ingredients[0], self.ingredient_cls)

    def test_add_ingredient_parameters(self):
        recipe_model = self.recipe_cls(ingredients=[])
        recipe_model.add_ingredient(title='test1', amount=1, unit='kg')

        assert recipe_model.ingredients[0].title == 'test1'
        assert recipe_model.ingredients[0].amount == 1
        assert recipe_model.ingredients[0].unit == 'kg'

    def test_add_ingredient_length_no_list(self):
        recipe_model = self.recipe_cls()
        recipe_model.add_ingredient(title='test1', amount=1, unit='kg')

        assert recipe_model.ingredients.count() == 1

    def test_add_ingredient_length_empty_list(self):
        recipe_model = self.recipe_cls(ingredients=[])
        recipe_model.add_ingredient(title='test1', amount=1, unit='kg')

        assert recipe_model.ingredients.count() == 1

    def test_add_ingredient_length_list_with_two(self):
        recipe_model = self.recipe_cls(ingredients=[self.ingredient_cls(), self.ingredient_cls()])
        recipe_model.add_ingredient(title='test1', amount=1, unit='kg')

        assert recipe_model.ingredients.count() == 3

    def test_add_ingredient_parameters_only_title(self):
        recipe_model = self.recipe_cls(ingredients=[])
        recipe_model.add_ingredient(title='test1')

        assert recipe_model.ingredients[0].title == 'test1'
        assert recipe_model.ingredients[0].amount is None
        assert recipe_model.ingredients[0].unit is None

    def test_clear_empty_ingredients_with_empty(self):
        recipe_model = self.recipe_cls(ingredients=[self.ingredient_cls(title='test1'), self.ingredient_cls(title=''),
                                                    self.ingredient_cls(title=None), self.ingredient_cls(title='test2'),
                                                    self.ingredient_cls(title=None)])
        recipe_model.clear_empty_ingredients()

        assert recipe_model.ingredients.count() == 2
        assert recipe_model.ingredients[0].title == 'test1'
        assert recipe_model.ingredients[1].title == 'test2'

    def test_clear_empty_ingredients_without_empty(self):
        recipe_model = self.recipe_cls(
            ingredients=[self.ingredient_cls(title='test1'), self.ingredient_cls(title='test2')])
        recipe_model.clear_empty_ingredients()

        assert recipe_model.ingredients.count() == 2
        assert recipe_model.ingredients[0].title == 'test1'
        assert recipe_model.ingredients[1].title == 'test2'


class TestWaitingRecipe(AbstractRecipeTests):
    recipe_cls = WaitingRecipe
    ingredient_cls = WaitingRecipeIngredient

    def test_reset_refused_sets_true_to_false(self):
        waiting_model = self.recipe_cls(refused=True)
        waiting_model.reset_refused()
        assert not waiting_model.refused

    def test_reset_refused_sets_false_to_false(self):
        waiting_model = self.recipe_cls(refused=False)
        waiting_model.reset_refused()
        assert not waiting_model.refused

    def test_reset_refused_sets_empty_to_false(self):
        waiting_model = self.recipe_cls()
        waiting_model.reset_refused()
        assert not waiting_model.refused

    def test_reject_sets_false_to_true(self):
        waiting_model = self.recipe_cls(refused=False)
        waiting_model.reject()
        assert waiting_model.refused

    def test_reject_sets_true_to_true(self):
        waiting_model = self.recipe_cls(refused=True)
        waiting_model.reject()
        assert waiting_model.refused

    def test_reject_sets_empty_to_true(self):
        waiting_model = self.recipe_cls()
        waiting_model.reject()
        assert waiting_model.refused


class TestRecipe(AbstractRecipeTests):
    recipe_cls = Recipe
    ingredient_cls = RecipeIngredient
