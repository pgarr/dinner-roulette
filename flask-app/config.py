import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


def get_app_admins():
    admins_string = os.environ.get('APP_ADMINS')
    try:
        return admins_string.split(',')
    except AttributeError:
        return []


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'very-hard-to-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = [os.environ.get('MAIL_ADDRESS')]
    LANGUAGES = ['en', 'pl']
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    APP_ADMINS = get_app_admins()
    BACKUP_SCHEDULE = os.environ.get('BACKUP_SCHEDULE') or None
    RECIPES_PER_PAGE = 15

    FRONT_URL = os.environ.get('FRONT_URL')
    RESET_PASSWORD_TOKEN_EXPIRES_IN = os.environ.get(
        'RESET_PASSWORD_TOKEN_EXPIRES_IN') or 15 * 600
