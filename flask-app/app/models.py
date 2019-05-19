from flask_login import UserMixin
from sqlalchemy.ext.declarative import declared_attr
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    admin = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(128))
    recipes = db.relationship('Recipe', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id_):
    return User.query.get(int(id_))


class RecipeMixin(object):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    time = db.Column(db.Integer)
    difficulty = db.Column(db.Integer)
    link = db.Column(db.String(1000))
    preparation = db.Column(db.Text)

    # TODO: attributes = db.relationship # one to many - attribute table

    @declared_attr
    def user_id(cls):
        return db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Recipe {}>'.format(self.title)

    # TODO: add_ingredient method


class IngredientMixin(object):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float)
    unit = db.Column(db.String(20))

    def __repr__(self):
        return '<RecipeIngredient {} from {}>'.format(self.title, self.recipe_id)


class Recipe(RecipeMixin, db.Model):
    __tablename__ = 'recipe'

    ingredients = db.relationship('RecipeIngredient', lazy="dynamic", cascade="all, delete-orphan")


class RecipeIngredient(IngredientMixin, db.Model):
    __tablename__ = 'recipe_ingredient'

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))


class WaitingRecipe(RecipeMixin, db.Model):
    __tablename__ = 'waiting_recipe'

    ingredients = db.relationship('WaitingRecipeIngredient', lazy="dynamic", cascade="all, delete-orphan")


class WaitingRecipeIngredient(IngredientMixin, db.Model):
    __tablename__ = 'waiting_recipe_ingredient'

    recipe_id = db.Column(db.Integer, db.ForeignKey('waiting_recipe.id'))
