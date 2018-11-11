from db import db


class RecipeDetailModel(db.Model):
    __tablename__ = 'recipe_detail'

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(1000))
    description = db.Column(db.Text())

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'link': self.link, 'description': self.description}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
