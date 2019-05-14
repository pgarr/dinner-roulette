from app.models import User, load_user


def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user


def identity(payload):
    user_id = payload['identity']
    return load_user(user_id)
