from sqlalchemy import ForeignKeyConstraint

from db import db


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
