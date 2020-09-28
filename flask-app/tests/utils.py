from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

    MAIL_SERVER = None
    MAIL_PORT = None
    MAIL_USERNAME = None
    MAIL_PASSWORD = None

    RECIPES_PER_PAGE = 4
    ELASTICSEARCH_URL = None
