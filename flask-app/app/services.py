from sqlalchemy.orm import load_only

from app import db
from app.models import Recipe, RecipeIngredient


def init_recipe(author):  # TODO: kwargs
    return Recipe(ingredients=[RecipeIngredient()], author=author)


def save_recipe(model):
    model.ingredients = list(filter(lambda ingredient: ingredient.title, model.ingredients))
    db.session.add(model)
    db.session.commit()


def get_recipe(pk):
    return Recipe.query.get_or_404(pk)


def get_all_recipes():
    return Recipe.query.options(load_only("id", "title", "time", "difficulty")).all()
