from threading import Thread
from flask import current_app
from flask_mail import Message


def send_async_email(fl_app, msg):
    with fl_app.app_context():
        from app import mail
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body, attachment_tuple=None):
    """attachment_tuple - (filename, content_type, data)"""
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    try:
        msg.attach(filename=attachment_tuple[0], content_type=attachment_tuple[1],
                   data=attachment_tuple[2])  # TODO: use named tuple
    except Exception:
        pass
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()
