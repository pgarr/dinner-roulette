from sqlalchemy.orm import load_only

from app import db
from app.models import Recipe, WaitingRecipe, WaitingRecipeIngredient


def init_waiting_recipe(author):  # TODO: kwargs
    return WaitingRecipe(ingredients=[WaitingRecipeIngredient()], author=author)


def save_recipe(model):
    model.ingredients = list(filter(lambda ingredient: ingredient.title, model.ingredients))
    db.session.add(model)
    db.session.commit()


def get_recipe(pk):
    return Recipe.query.get_or_404(pk)


def get_waiting_recipe(pk):
    return WaitingRecipe.query.get_or_404(pk)


def get_all_recipes():
    return Recipe.query.options(load_only("id", "title", "time", "difficulty")).all()
