import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler


def set_smtp_handler(config, level=logging.ERROR):
    auth = None
    if config['MAIL_USERNAME'] or config['MAIL_PASSWORD']:
        auth = (config['MAIL_USERNAME'], config['MAIL_PASSWORD'])
    secure = None
    if config['MAIL_USE_TLS']:
        secure = ()
    handler = SMTPHandler(
        mailhost=(config['MAIL_SERVER'], config['MAIL_PORT']),
        fromaddr='no-reply@' + config['MAIL_SERVER'],
        toaddrs=config['ADMINS'], subject='Dinner-roulette Failure',
        credentials=auth, secure=secure)
    handler.setLevel(level)

    return handler


def set_stdout_logger(level=logging.INFO):
    handler = logging.StreamHandler()
    handler.setLevel(level)
    return handler


def register_handler(app, module_loggers, handler):
    app.logger.addHandler(handler)
    for logger_name in module_loggers:
        logger = logging.getLogger(logger_name)
        logger.addHandler(handler)


def register_file_loggers(app, module_loggers):
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    if not os.path.exists('logs'):
        os.mkdir('logs')

    app_handler = RotatingFileHandler('logs/smog-api.log', maxBytes=102400, backupCount=100)
    app_handler.setFormatter(formatter)

    app.logger.addHandler(app_handler)
    for logger_name in module_loggers:
        module_handler = RotatingFileHandler('logs/' + logger_name + '.log', maxBytes=102400, backupCount=100)
        module_handler.setFormatter(formatter)
        logger = logging.getLogger(logger_name)
        logger.addHandler(module_handler)
