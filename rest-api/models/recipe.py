from db import db


class RecipeModel(db.Model):
    __tablename__ = 'recipe'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    ingredients = db.relationship('RecipeIngredientModel', lazy='dynamic')
    detail = db.relationship('RecipeDetailModel', uselist=False, back_populates='recipe')

    def __init__(self, name):
        self.name = name

    def json_with_lazy(self):
        return {'name': self.name, "ingredients": [ingredient.json() for ingredient in self.ingredients.all()],
                "detail": self.detail.json()}

    def json(self):
        return {'name': self.name}

    @classmethod
    def find_by_id(cls, id_):
        return cls.query.get(id_)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
