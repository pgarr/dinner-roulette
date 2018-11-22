from db import db


class RecipeDetail(db.Model):
    __tablename__ = 'recipe_detail'

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(1000))
    description = db.Column(db.Text())
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    recipe = db.relationship("Recipe", back_populates="detail")
