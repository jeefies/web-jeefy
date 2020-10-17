from threading import Thread
from flask import current_app
from . import mail

def _send_email(ctx, msg):
    ctx.push()
    mail.send(msg)
    ctx.pop()

def send_email(msg):
    #app = current_app.get_current_object()
    ctx = current_app.app_context()
    return Thread(target=_send_email, args=(ctx, msg)).start()
