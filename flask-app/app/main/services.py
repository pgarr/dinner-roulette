from flask_login import current_user

from app import db
from app.models import Recipe, RecipeDetail, RecipeIngredient


def init_recipe():
    return Recipe(detail=RecipeDetail(), ingredients=[RecipeIngredient()])


def save_recipe(model):
    model.ingredients = list(filter(lambda ingredient: ingredient.title, model.ingredients))
    db.session.add(model)
    db.session.commit()


def get_recipe(pk):
    return Recipe.query.get_or_404(pk)


def save_recipe_from_form(form, model):
    model.title = form.title.data
    model.time = form.time.data
    model.difficulty = form.difficulty.data
    model.detail.link = form.detail.link.data
    model.detail.preparation = form.detail.preparation.data
    model.ingredients = []
    for i in form.ingredients:
        if i.title.data:
            recipe_ingredient_model = RecipeIngredient(
                title=i.title.data,
                amount=i.amount.data,
                unit=i.unit.data
            )
            model.ingredients.append(recipe_ingredient_model)
    model.author = current_user
    save_recipe(model)
