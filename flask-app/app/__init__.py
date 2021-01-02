import logging

from elasticsearch import Elasticsearch
from flask import Flask, current_app, request
from flask_babel import Babel
from flask_cors import CORS
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.utils.loggers import set_smtp_handler, register_handler, set_stdout_logger, register_file_loggers
from config import Config

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
babel = Babel()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.app_context().push()

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    babel.init_app(app)

    CORS(app)

    from app.blueprints.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.blueprints.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from app.blueprints.api_auth import bp as api_auth_bp
    app.register_blueprint(api_auth_bp, url_prefix='/api/auth')

    from app.blueprints.api_admin import bp as api_admin_bp
    app.register_blueprint(api_admin_bp, url_prefix='/api/admin')

    # elasticsearch
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None

    # loggers
    module_loggers = ['sqlalchemy', 'backup']

    if not app.debug and not app.testing:
        # mail errors
        if app.config['MAIL_SERVER']:
            handler = set_smtp_handler(app.config, level=logging.ERROR)
            register_handler(app, module_loggers, handler)

        # stdout loggers
        if app.config['LOG_TO_STDOUT']:
            handler = set_stdout_logger(level=logging.INFO)
            register_handler(app, module_loggers, handler)

        # file loggers
        else:
            register_file_loggers(app, module_loggers)

        app.logger.setLevel(logging.INFO)
        app.logger.info('dinner-roulette startup')

    return app


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])


from app.models import auth, recipes
