from db import db


class Recipe(db.Model):
    __tablename__ = 'recipe'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    detail = db.relationship("RecipeDetail", uselist=False, back_populates="recipe", lazy="dynamic")
    ingredients = db.relationship('RecipeIngredient', lazy="dynamic")
