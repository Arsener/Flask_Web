from flask import current_app, render_template
from flask_mail import Message
from threading import Thread
from . import mail



def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(email, name):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' Welcome to Flask Web!',
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[email])
    msg.html = render_template('new_user.html', name = name)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr