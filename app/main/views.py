import os
import time
import hashlib

from flask import url_for, Flask, render_template, redirect, session, flash, request
from flask import make_response as mkresp

from . import main
from .. import mail
from ..sdmail import send_email
from .forms import NameForm, LogoutForm, LoginForm, RegisterForm
from .now import now

from jeefies.flask_self import protect, render, Login, Logout, get_user, gravatar, emailmsg
from jeefies import Content, Hexsec

from flask_mail import Message

req = request
conpath = os.path.dirname(os.path.dirname(__file__))

conuser = Content(conpath, 'user')

@main.route('/')
def index():
    t = now()
    return render('greet.html', tm=t)


@main.route('/login', methods=['GET', "POST"])
def login():
    form = LoginForm()
    t = now()

    if form.validate_on_submit():
        user_name = form.name.data
        #print(user_name, con.has(user_name))
        user = conuser.get(user_name)

        if user is None:
            flash('No such user')
            return redirect(url_for('.login'))
        if len(user[1]) == 1:
            user = conuser.get(user[1][0])
            user_name = user[0]
        inpw = form.password.data
        if not Hexsec.decrypt(user[1][0]) == inpw:
            #print(Hexsec.decrypt(user[1][0]))
            flash('Error Password, please try again')
            return redirect(url_for('.login'))

        return Login(redirect('/'), user_name, form.password.data, conpath)

    return render('ask_name.html', form=form, tm=t)


def director():
    flash('You must be logined, click the button on the left side on the top to login')
    return redirect(url_for('.index'))


@main.route('/logout', methods=['GET', 'POST'])
@protect(director, conpath)
def logout():
    form = LogoutForm()
    if form.sure.data:
        resp = mkresp(Logout(redirect('/')))
        for cook in req.cookies:
            if req.cookies.get(cook).endswith('in'):
                resp.delete_cookie(cook)
        return resp
    return render('logingout.html', name=session.get(req.remote_addr), form=form)

from jeefies import Hashsec
@main.route('/regist', methods=['GET', 'POST'])
def registor():
    form = RegisterForm()
    if form.validate_on_submit():
        #con = Content(conpath, 'user')
        con = conuser
        if con.has(form.username.data):
            flash('User name is userd, please change a name')
            return redirect(url_for('.registor'))
        passwords = Content(conpath, 'passwd').allitem()
        for password in passwords:
            passwd = password[1][0]
            if passwd == form.regist_passwd.data:
                permission = password[0]
                break
        else:
            flash('Please enter the right regist password or ask author for help')
            return redirect(url_for('.registor'))
        # email, [name, passwd, permission]
        # name, [passwd, permission, email, full_name, discription]; email, [name]
        url = Hexsec.encrypt(form.email.data)
        url = url_for('.activate',token=url, _external=True)
        flash('Please wait a moment, the email is sending')
        send_email(emailmsg(form.email.data, \
                'Activate your Account', 'email/activate', \
                name=form.username.data, acturl=url))
        con.add(form.email.data, [form.username.data, Hexsec.encrypt(form.password.data), permission])
        flash('Please check your email to activate your user')
        return redirect(url_for('.index'))
    return render('regist.html', form=form, name=session.get(req.remote_addr))

@main.route('/regist/<token>')
def activate(token):
    con = conuser
    email = Hexsec.decrypt(token)
    if con.has(email):
        acc = con.get(email)
        con.add(acc[1][0], [acc[1][1], acc[1][2], email, '', '', ''])
        con.set(email, [acc[1][0]])
        flash('You can login now!')
        return redirect(url_for('.login'))
    return redirect(404)


@main.route('/check')
@protect(director, conpath)
def testing():
    return render('base.html', pkgs={'aa': 'aa'}, dirs={'bb': 'bb'}, args=[req.remote_addr, req.cookies])
