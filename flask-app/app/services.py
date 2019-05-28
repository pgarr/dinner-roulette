from sqlalchemy.orm import load_only

from app import db
from app.models import Recipe, WaitingRecipe


def init_waiting_recipe(**kwargs):
    return WaitingRecipe(**kwargs)


def clone_recipe_to_waiting(recipe_model):
    waiting_model = WaitingRecipe(title=recipe_model.title,
                                  time=recipe_model.time,
                                  difficulty=recipe_model.difficulty,
                                  link=recipe_model.link,
                                  preparation=recipe_model.preparation,
                                  author=recipe_model.author,
                                  updated_recipe=recipe_model)
    for i in recipe_model.ingredients:
        waiting_model.add_ingredient(title=i.title, amount=i.amount, unit=i.unit)
    return waiting_model


def accept_waiting(waiting_model):
    recipe_model = _push_updates_to_recipe(waiting_model)
    db.session.add(recipe_model)
    db.session.delete(waiting_model)
    db.session.commit()
    return recipe_model


def _push_updates_to_recipe(waiting_model):
    if waiting_model.updated_recipe:
        recipe_model = waiting_model.updated_recipe
    else:
        recipe_model = Recipe(author=waiting_model.author)
    recipe_model.title = waiting_model.title
    recipe_model.time = waiting_model.time
    recipe_model.difficulty = waiting_model.difficulty
    recipe_model.link = waiting_model.link
    recipe_model.preparation = waiting_model.preparation
    recipe_model.ingredients = []
    for i in waiting_model.ingredients:
        recipe_model.add_ingredient(title=i.title, amount=i.amount, unit=i.unit)
    return recipe_model


def save_recipe(model):
    model.clear_empty_ingredients()
    db.session.add(model)
    db.session.commit()


def get_recipe(pk):
    return Recipe.query.get_or_404(pk)


def get_waiting_recipe(pk):
    return WaitingRecipe.query.get_or_404(pk)


def get_all_recipes():
    return Recipe.query.options(load_only("id", "title", "time", "difficulty")).all()


def get_all_waiting_recipes(user):
    if user.admin:
        waiting_recipes = WaitingRecipe.query.options(load_only("id", "title", "time", "difficulty")).all()
    else:
        waiting_recipes = WaitingRecipe.query.filter(WaitingRecipe.author == user).options(
            load_only("id", "title", "time", "difficulty")).all()
    return waiting_recipes
