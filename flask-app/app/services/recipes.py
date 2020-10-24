from flask import current_app
from sqlalchemy import desc, asc
from sqlalchemy.orm import load_only

from app import db
from app.models.recipes import WaitingRecipe, Recipe
from app.utils.helpers import page_handler


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
    current_app.logger.info('ID %d waiting recipe accepted to ID %d recipe' % (waiting_model.id, recipe_model.id))
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
    try:
        model.reset_refused()
    except AttributeError:
        pass
    db.session.add(model)
    db.session.commit()
    current_app.logger.info('%s saved - ID %d' % (model.__class__, model.id))


def get_recipe(pk):
    recipe = Recipe.query.get_or_404(pk)
    current_app.logger.debug('Recipe got ID %d' % recipe.id)
    return recipe


def get_waiting_recipe(pk):
    waiting_recipe = WaitingRecipe.query.get_or_404(pk)
    current_app.logger.debug('Waiting recipe got ID %d' % waiting_recipe.id)
    return waiting_recipe


def get_recipes(page, per_page):
    page, per_page = page_handler(page, per_page)

    paginated = Recipe.query.options(load_only("id", "title", "time", "difficulty")).order_by(
        desc(Recipe.create_date)).paginate(page, per_page, False)
    current_app.logger.debug('Page %d of list of recipes got' % page)
    return paginated


def get_user_recipes(author, page, per_page):
    paginated = Recipe.query.filter(Recipe.author == author).options(
        load_only("id", "title", "time", "difficulty")).order_by(desc(Recipe.create_date)).paginate(page, per_page,
                                                                                                    False)
    current_app.logger.debug("Page %d of list of %s's recipes got" % (page, author.username))
    return paginated


def get_waiting_recipes(user, page, per_page):
    if user.admin:  # TODO: DRY - if else are nearly same
        paginated = WaitingRecipe.query \
            .filter(WaitingRecipe.refused == False) \
            .options(load_only("id", "title", "time", "difficulty")) \
            .order_by(asc(WaitingRecipe.last_modified)) \
            .paginate(page, per_page, False)
        # smth == False is not pytonic, but required for model property. Nothing else works.
    else:
        paginated = WaitingRecipe.query \
            .filter(WaitingRecipe.author == user) \
            .options(load_only("id", "title", "time", "difficulty", "refused")) \
            .order_by(asc(WaitingRecipe.last_modified)) \
            .paginate(page, per_page, False)
    current_app.logger.debug('"Page %d of list of waiting recipes got for user %s' % (page, user.username))
    return paginated


def get_recipe_by_title(title):
    return Recipe.query.filter_by(title=title).first()


def reject_waiting(waiting_model):
    waiting_model.reject()
    db.session.add(waiting_model)
    db.session.commit()
    current_app.logger.info('Pending recipe refused - ID %d' % waiting_model.id)
    return waiting_model
