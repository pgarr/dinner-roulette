from time import time

import jwt
from flask import current_app
from flask_login import UserMixin
from sqlalchemy.ext.declarative import declared_attr
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    @property
    def admin(self):
        return self.username in current_app.config['APP_ADMINS']

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id_ = jwt.decode(token, current_app.config['SECRET_KEY'],
                             algorithms=['HS256'])['reset_password']
        except Exception:
            return
        return User.query.get(id_)


@login.user_loader
def load_user(id_):
    return User.query.get(int(id_))


class IngredientMixin(object):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float)
    unit = db.Column(db.String(20))

    def __repr__(self):
        return '<RecipeIngredient {} from {}>'.format(self.title, self.recipe_id)


class RecipeMixin(object):
    ingredient_class = IngredientMixin

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    time = db.Column(db.Integer)
    difficulty = db.Column(db.Integer)
    link = db.Column(db.String(1000))
    preparation = db.Column(db.Text)

    # TODO: attributes = db.relationship # one to many - attribute table

    @declared_attr
    def author_id(cls):
        return db.Column(db.Integer, db.ForeignKey('user.id'))

    @declared_attr
    def author(cls):
        return db.relationship("User")

    def __repr__(self):
        return '<Recipe {}>'.format(self.title)

    def add_ingredient(self, **kwargs):
        if not self.ingredients:
            self.ingredients = []
        self.ingredients.append(self.ingredient_class(**kwargs))

    def clear_empty_ingredients(self):
        self.ingredients = list(filter(lambda ingredient: ingredient.title, self.ingredients))


class RecipeIngredient(IngredientMixin, db.Model):
    __tablename__ = 'recipe_ingredient'

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))


class Recipe(RecipeMixin, db.Model):
    __tablename__ = 'recipe'

    ingredient_class = RecipeIngredient
    ingredients = db.relationship(ingredient_class, lazy="dynamic", cascade="all, delete-orphan")
    waiting_updates = db.relationship("WaitingRecipe", uselist=False, back_populates="updated_recipe")


class WaitingRecipeIngredient(IngredientMixin, db.Model):
    __tablename__ = 'waiting_recipe_ingredient'

    recipe_id = db.Column(db.Integer, db.ForeignKey('waiting_recipe.id'))


class WaitingRecipe(RecipeMixin, db.Model):
    __tablename__ = 'waiting_recipe'

    ingredient_class = WaitingRecipeIngredient
    ingredients = db.relationship(ingredient_class, lazy="dynamic", cascade="all, delete-orphan")
    # TODO: przenieść do mixin
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    updated_recipe = db.relationship("Recipe", back_populates="waiting_updates")
