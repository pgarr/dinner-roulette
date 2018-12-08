from flask import current_app

from app import db


class Recipe(db.Model):
    __tablename__ = 'recipe'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    detail = db.relationship("RecipeDetail", uselist=False, back_populates="recipe", cascade="all, delete-orphan")
    ingredients = db.relationship('RecipeIngredient', lazy="dynamic", cascade="all, delete-orphan")


class RecipeDetail(db.Model):
    __tablename__ = 'recipe_detail'

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(1000))
    description = db.Column(db.Text)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    recipe = db.relationship("Recipe", back_populates="detail")


class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredient'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer)
    unit = db.Column(db.String(20))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    info = db.relationship("IngredientInfo", uselist=False, foreign_keys=[name],
                           primaryjoin="RecipeIngredient.name==IngredientInfo.name", lazy="joined")


class IngredientInfo(db.Model):
    __tablename__ = 'ingredient_info'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    calories_per_gram = db.Column(db.Integer)
    unit_multipliers = db.relationship('IngredientUnitMultiplier', lazy="joined", cascade="all, delete-orphan")


class IngredientUnitMultiplier(db.Model):
    __tablename__ = 'ingredient_unit_multiplier'

    id = db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.String(50), nullable=False)
    multiplier = db.Column(db.Float, nullable=False)
    ingredient_info_id = db.Column(db.Integer, db.ForeignKey('ingredient_info.id'))
