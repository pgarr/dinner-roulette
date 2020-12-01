from flask import current_app, render_template
from flask_babel import _

from app.utils.email import send_email


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    reset_url = current_app.config['FRONT_URL'] + '/reset_password/' + token
    send_email(_('[Dinner-roulette] Reset Your Password'),
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt', user=user, reset_url=reset_url),
               html_body=render_template('email/reset_password.html', user=user, reset_url=reset_url))
    current_app.logger.info('%s requested password reset' % user.username)
