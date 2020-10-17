from . import user

from flask import url_for, redirect, render_template, flash, make_response, request
mkresp = make_response; req = request

from jeefies import Content
from jeefies.flask_self import protect, get_user, gravatar, permission

import os
import hashlib

base = os.path.abspath(os.path.dirname(__file__))
conpath = os.path.split(base)[0]

con = Content(conpath, 'user')

def loginerror():
    flash('You must be logined!')
    return redirect(url_for('main.login'))

pro = protect(loginerror, conpath)

@user.route('/user')
@pro
def index():
    accuser = con.get(get_user())
    img = gravatar(accuser[1][2], 256)
    disc = accuser[1][-1]
    disc = [disc] if disc.split('\n') == disc else disc.split('\n')
    return render_template('user/index.html', acc=accuser, img=img, self=True, disc=disc)

@user.route('/user/<string:username>')
def show_one(username):
    "show one user's info by the name or the email"
    '''
    try:
        int(username)
        flash('No such user')
        return redirect(url_for('.index'))
    except:
        pass
    '''
    if not con.has(username):
        flash("No such user")
        return redirect(urk_for('.index'))
    accuser = con.get(username)
    if len(accuser[1]) == 1:
        accuser = con.get(accuser[1][0])
    # name, [passwd, permission, email, full_name, discription]
    img = gravatar(accuser[1][2], 256)
    disc = accuser[1][-1]
    if disc.split('\n') == disc:
        disc = [disc]
    else:
        disc = disc.split('\n')
    if username == get_user():
        self = True
    else:
        self = False
    return render_template('user/index.html', img=img, disc=disc, self=self, acc=accuser)

@user.route('/users/list')
@permission(16, lambda:redirect(url_for('.index')), conpath)
def listusers():
    l = '<p>{}</p>'
    turn = '<div><li>{}</li></div>'
    each = ''
    for name in con.allname():
        if not len(con.get(name)[1]) == 1:
            each += l.format(name)
    return turn.format(each)

@user.route('/user/<string:username>/acc')
def edit_profile(username):
    if not con.has(username):
        return redirect(404)
    else:
        return redirect(url_for('user.acc'))
