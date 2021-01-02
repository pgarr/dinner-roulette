from flask import current_app, render_template
from flask_babel import _
from flask_jwt_extended import create_access_token, create_refresh_token

from app.services.auth import get_user_by_name
from app.utils.email import send_email


def get_fresh_jwt_token(username, password, with_refresh_token=False):
    user = get_user_by_name(username)
    if user and user.check_password(password):
        ret = {
            'access_token': create_access_token(identity=user, fresh=True),
        }
        if with_refresh_token:
            ret['refresh_token'] = create_refresh_token(identity=user)
        return ret
    return None


def send_password_reset_email(user):
    token = user.get_reset_password_token(current_app.config['RESET_PASSWORD_TOKEN_EXPIRES_IN'])
    reset_url = current_app.config['FRONT_URL'] + '/reset_password/' + token
    send_email(_('[Dinner-roulette] Reset Your Password'),
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt', user=user, reset_url=reset_url),
               html_body=render_template('email/reset_password.html', user=user, reset_url=reset_url))
    current_app.logger.info('%s requested password reset' % user.username)