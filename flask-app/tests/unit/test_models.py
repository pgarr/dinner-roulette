from unittest import TestCase

from app.models import Recipe, RecipeIngredient, WaitingRecipe, WaitingRecipeIngredient


class TestAbstractRecipe(object):
    recipe_cls = None
    ingredient_cls = None

    def test_add_ingredient_class(self):
        recipe_model = self.recipe_cls(ingredients=[])
        recipe_model.add_ingredient(title='test1', amount=1, unit='kg')
        self.assertIsInstance(recipe_model.ingredients[0], self.ingredient_cls)

    def test_add_ingredient_parameters(self):
        recipe_model = self.recipe_cls(ingredients=[])
        recipe_model.add_ingredient(title='test1', amount=1, unit='kg')

        self.assertEqual(recipe_model.ingredients[0].title, 'test1')
        self.assertEqual(recipe_model.ingredients[0].amount, 1)
        self.assertEqual(recipe_model.ingredients[0].unit, 'kg')

    def test_add_ingredient_length_no_list(self):
        recipe_model = self.recipe_cls()
        recipe_model.add_ingredient(title='test1', amount=1, unit='kg')

        self.assertEqual(recipe_model.ingredients.count(), 1)

    def test_add_ingredient_length_empty_list(self):
        recipe_model = self.recipe_cls(ingredients=[])
        recipe_model.add_ingredient(title='test1', amount=1, unit='kg')

        self.assertEqual(recipe_model.ingredients.count(), 1)

    def test_add_ingredient_length_list_with_two(self):
        recipe_model = self.recipe_cls(ingredients=[self.ingredient_cls(), self.ingredient_cls()])
        recipe_model.add_ingredient(title='test1', amount=1, unit='kg')

        self.assertEqual(recipe_model.ingredients.count(), 3)

    def test_add_ingredient_parameters_only_title(self):
        recipe_model = self.recipe_cls(ingredients=[])
        recipe_model.add_ingredient(title='test1')

        self.assertEqual(recipe_model.ingredients[0].title, 'test1')
        self.assertEqual(recipe_model.ingredients[0].amount, None)
        self.assertEqual(recipe_model.ingredients[0].unit, None)


class TestWaitingRecipe(TestAbstractRecipe, TestCase):
    recipe_cls = Recipe
    ingredient_cls = RecipeIngredient


class TestRecipe(TestAbstractRecipe, TestCase):
    recipe_cls = WaitingRecipe
    ingredient_cls = WaitingRecipeIngredient
