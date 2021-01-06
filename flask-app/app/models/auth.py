from time import time

import jwt
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    recipes = db.relationship('Recipe', back_populates='author')

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

    def __eq__(self, other):
        if isinstance(other, User):
            return self.id == other.id
        else:
            return False

    def __ne__(self, other):
        equal = self.__eq__(other)
        return not equal
