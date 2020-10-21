from app import db
from app.models.auth import User


def get_user_by_name(username):
    return User.query.filter_by(username=username).first()


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


# TODO: Tests
def create_user(username, email, password):
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


# TODO: Tests
def verify_reset_password_token(token):
    return User.verify_reset_password_token(token)


def set_new_password(user, password):
    user.set_password(password)
    db.session.commit()
