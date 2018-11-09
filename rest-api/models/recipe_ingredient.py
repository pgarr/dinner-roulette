from db import db


# Association table
class RecipeIngredientModel(db.Model):
    __tablename__ = 'recipe_ingredient'

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
    amount = db.Column(db.Integer)
    unit = db.Column(db.String(50))
    ingredient = db.relationship('IngredientModel')

    def __init__(self, amount, unit):
        self.amount = amount
        self.unit = unit

    def json(self):
        return {'name': self.ingredient.name, 'amount': self.amount, 'unit': self.unit}
