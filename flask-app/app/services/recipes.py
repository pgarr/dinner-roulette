from flask import current_app
from sqlalchemy import desc, asc
from sqlalchemy.orm import load_only

from app import db
from app.models.recipe import Recipe, StatusEnum
from app.utils.helpers import page_handler


def init_recipe(author, **kwargs):
    return Recipe(author=author, **kwargs)


def accept_recipe(model):
    model.accept()
    db.session.add(model)
    db.session.commit()
    current_app.logger.info('Recipe accepted - ID %d' % model.id)
    return model


def save_recipe(model):
    model.clear_empty_ingredients()
    model.reset_status()
    db.session.add(model)
    db.session.commit()
    current_app.logger.info('Recipe saved - ID %d' % model.id)
    return model


def get_recipe(pk):
    model = Recipe.query.get_or_404(pk)
    current_app.logger.debug('Recipe got - ID %d' % model.id)
    return model


def get_accepted_recipes(page, per_page):
    page, per_page = page_handler(page, per_page)

    paginated = Recipe.query.filter(Recipe.status == StatusEnum.accepted).options(
        load_only("id", "title", "time", "difficulty", "status")).order_by(
        desc(Recipe.create_date)).paginate(page, per_page, False)
    current_app.logger.debug('Recipes got - page %d - accepted' % page)
    return paginated


def get_user_recipes(author, page, per_page):
    page, per_page = page_handler(page, per_page)

    paginated = Recipe.query.filter(Recipe.author == author).options(
        load_only("id", "title", "time", "difficulty", "status")).order_by(
        desc(Recipe.create_date)).paginate(page, per_page, False)
    current_app.logger.debug('Recipes got - page %d - user %s' % (page, author.username))
    return paginated


def get_pending_recipes(page, per_page):
    page, per_page = page_handler(page, per_page)

    paginated = Recipe.query.filter(Recipe.status == StatusEnum.pending).options(
        load_only("id", "title", "time", "difficulty", "status")).order_by(
        asc(Recipe.last_modified)).paginate(page, per_page, False)
    current_app.logger.debug('Recipes got - page %d - pending' % page)
    return paginated


def get_recipes(page, per_page, filters):
    page, per_page = page_handler(page, per_page)
    # TODO: generic method with applicable filters
    paginated = Recipe.query.filter().options(
        load_only("id", "title", "time", "difficulty", "status")).order_by(
        asc(Recipe.create_date)).paginate(page, per_page, False)


def get_recipe_by_title(title):
    return Recipe.query.filter_by(title=title).first()


def reject_recipe(model):
    model.reject()
    db.session.add(model)
    db.session.commit()
    current_app.logger.info('Recipe refused - ID %d' % model.id)
    return model


def get_full_all_recipes():
    recipes = Recipe.query.all()
    return recipes
