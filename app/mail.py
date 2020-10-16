from threading import Thread
from flask import current_app
from . import mail

def _send_email(app, ctx, msg):
    ctx.push()
    with app.app_context():
        mail.send(msg)
    ctx.pop()

def send_email(msg):
    app = current_app#.get_current_object()
    ctx = current_app.app_context()
    return Thread(target=_send_email, args=(app, ctx, msg)).start()
