from flask import current_app
from sqlalchemy.orm import load_only

from app import db
from app.models import Recipe, WaitingRecipe, User


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
    w_id = waiting_model.id
    db.session.delete(waiting_model)
    db.session.commit()
    current_app.logger.info('ID %d waiting recipe accepted to ID %d recipe' % (w_id, recipe_model.id))
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
    current_app.logger.info('%s saved - ID %d' % (type(model.__class__), model.id))


def get_recipe(pk):
    recipe = Recipe.query.get_or_404(pk)
    current_app.logger.debug('Recipe got ID %d' % recipe.id)
    return recipe


def get_waiting_recipe(pk):
    waiting_recipe = WaitingRecipe.query.get_or_404(pk)
    current_app.logger.debug('Waiting recipe got ID %d' % waiting_recipe.id)
    return waiting_recipe


def get_all_recipes():
    recipes = Recipe.query.options(load_only("id", "title", "time", "difficulty")).all()
    current_app.logger.debug('Full list of recipes got')
    return recipes


def get_user_recipes(author):
    recipes = Recipe.query.filter(Recipe.author == author).options(load_only("id", "title", "time", "difficulty")).all()
    current_app.logger.debug("List of %s's recipes got" % author.username)
    return recipes


def get_all_waiting_recipes(user):
    if user.admin:
        waiting_recipes = WaitingRecipe.query.options(load_only("id", "title", "time", "difficulty")).all()
    else:
        waiting_recipes = WaitingRecipe.query.filter(WaitingRecipe.author == user).options(
            load_only("id", "title", "time", "difficulty")).all()
    current_app.logger.debug('Full list of waiting recipes got for user %s' % user.username)
    return waiting_recipes


def get_user_by_name(username):
    return User.query.filter_by(username=username).first()
