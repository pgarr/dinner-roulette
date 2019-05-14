from app import db
from app.models import Recipe, RecipeDetail, RecipeIngredient


def init_recipe(author=None):
    return Recipe(detail=RecipeDetail(), ingredients=[RecipeIngredient()], author=author)


def save_recipe(model):
    model.ingredients = list(filter(lambda ingredient: ingredient.title, model.ingredients))
    db.session.add(model)
    db.session.commit()


def get_recipe(pk):
    return Recipe.query.get_or_404(pk)



