from sqlalchemy.orm import load_only

from app import db
from app.models import Recipe, WaitingRecipe


def init_waiting_recipe(**kwargs):  # TODO: kwargs
    return WaitingRecipe(**kwargs)


def clone_recipe_to_waiting(recipe_model):
    waiting_model = WaitingRecipe(title=recipe_model.title,
                                  time=recipe_model.time,
                                  difficulty=recipe_model.difficulty,
                                  link=recipe_model.link,
                                  preparation=recipe_model.preparation,
                                  author=recipe_model.author)
    for i in recipe_model.ingredients:
        waiting_model.add_ingredient(title=i.title, amount=i.amount, unit=i.unit)
    return waiting_model


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
