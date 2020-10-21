from app import db
from app.models.mixins.recipes import IngredientMixin, RecipeMixin
from app.models.mixins.search import SearchableMixin


class RecipeIngredient(IngredientMixin, db.Model):
    __tablename__ = 'recipe_ingredient'

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))


class Recipe(RecipeMixin, SearchableMixin, db.Model):
    __tablename__ = 'recipe'

    ingredient_class = RecipeIngredient
    waiting_updates = db.relationship("WaitingRecipe", uselist=False, back_populates="updated_recipe")


class WaitingRecipeIngredient(IngredientMixin, db.Model):
    __tablename__ = 'waiting_recipe_ingredient'

    recipe_id = db.Column(db.Integer, db.ForeignKey('waiting_recipe.id'))


class WaitingRecipe(RecipeMixin, db.Model):
    __tablename__ = 'waiting_recipe'

    ingredient_class = WaitingRecipeIngredient
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    updated_recipe = db.relationship("Recipe", back_populates="waiting_updates")
    refused = db.Column(db.Boolean, default=False)

    def reset_refused(self):
        self.refused = False

    def reject(self):
        self.refused = True
