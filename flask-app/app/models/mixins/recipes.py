from datetime import datetime
from sqlalchemy.ext.declarative import declared_attr

from app import db


class IngredientMixin(object):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float)
    unit = db.Column(db.String(20))

    def __repr__(self):
        return '<RecipeIngredient {} from {}>'.format(self.title, self.recipe_id)


class RecipeMixin(object):
    __searchable__ = ['title']
    ingredient_class = IngredientMixin

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    time = db.Column(db.Integer)
    difficulty = db.Column(db.Integer)
    link = db.Column(db.String(1000))
    preparation = db.Column(db.Text)
    create_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    last_modified = db.Column(db.DateTime, index=True, onupdate=datetime.utcnow)

    @declared_attr
    def author_id(cls):
        return db.Column(db.Integer, db.ForeignKey('user.id'))

    @declared_attr
    def author(cls):
        return db.relationship("User")

    @declared_attr
    def ingredients(cls):
        return db.relationship(cls.ingredient_class, lazy="dynamic", cascade="all, delete-orphan")

    def __repr__(self):
        return '<Recipe {}>'.format(self.title)

    def add_ingredient(self, **kwargs):
        if not self.ingredients:
            self.ingredients = []
        self.ingredients.append(self.ingredient_class(**kwargs))

    def clear_empty_ingredients(self):
        self.ingredients = list(filter(lambda ingredient: ingredient.title, self.ingredients))
