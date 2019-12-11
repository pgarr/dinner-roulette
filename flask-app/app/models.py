from datetime import datetime
from time import time

import jwt
from flask import current_app
from flask_login import UserMixin
from sqlalchemy.ext.declarative import declared_attr
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login
from app.search import query_index, add_to_index, remove_from_index


class SearchableMixin(object):
    """When attached to a model, will give it the ability to automatically manage an associated full-text index"""

    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):  # TODO: comprehension
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


# set up the event handlers
db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


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
        current_app.logger.info('Password changed for user %s' % self.username)
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
