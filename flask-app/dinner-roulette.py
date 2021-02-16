from app import create_app, db
from app.utils import cli
from app.models.user import User
from app.models.recipe import Recipe, RecipeIngredient

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Recipe': Recipe, 'Ingredient': RecipeIngredient}
