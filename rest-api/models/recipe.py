from db import db


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
