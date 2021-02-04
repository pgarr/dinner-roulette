import enum
from datetime import datetime

from app import db


class StatusEnum(enum.Enum):
    refused = -1
    pending = 0
    accepted = 1


class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredient'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float)
    unit = db.Column(db.String(20))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

    def __repr__(self):
        return '<RecipeIngredient {} from {}>'.format(self.title, self.recipe_id)


class Recipe(db.Model):
    __tablename__ = 'recipe'
    __searchable__ = ['title']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    time = db.Column(db.Integer)
    difficulty = db.Column(db.Integer)
    link = db.Column(db.String(1000))
    preparation = db.Column(db.Text)
    create_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    last_modified = db.Column(db.DateTime, index=True, onupdate=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', back_populates='recipes')
    ingredients = db.relationship(RecipeIngredient, cascade="all, delete-orphan")
    status = db.Column(db.Enum(StatusEnum), default=StatusEnum.pending)

    def __repr__(self):
        return '<Recipe {}>'.format(self.title)

    def __eq__(self, other):
        if isinstance(other, Recipe):
            return self.id == other.id
        else:
            return False

    def __ne__(self, other):
        equal = self.__eq__(other)
        return not equal

    def add_ingredient(self, **kwargs):
        if not self.ingredients:
            self.ingredients = []
        self.ingredients.append(RecipeIngredient(**kwargs))

    def clear_empty_ingredients(self):
        self.ingredients = list(filter(lambda ingredient: ingredient.title, self.ingredients))

    def accept(self):
        self.status = StatusEnum.accepted

    def reject(self):
        self.status = StatusEnum.refused

    def reset_status(self):
        self.status = StatusEnum.pending

    # TODO: tests
    def is_author_or_admin(self, user):
        if user is None:
            return False
        return user == self.author or user.admin
