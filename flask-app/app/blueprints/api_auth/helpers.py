from flask_jwt_extended import create_access_token, create_refresh_token

from app.services.auth import get_user_by_name


def get_fresh_jwt_token(username, password, with_refresh_token=False):
    user = get_user_by_name(username)
    if user and user.check_password(password):
        ret = {
            'access_token': create_access_token(identity=user.username, fresh=True),
        }
        if with_refresh_token:
            ret['refresh_token'] = create_refresh_token(identity=user.username)
        return ret
    return None

