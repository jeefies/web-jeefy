import os
from datetime import datetime
import time
from .now import now
from flask import url_for, Flask, render_template, redirect, session, flash,request
from flask import make_response as mkresp
from . import main
from .forms import NameForm, LogoutForm, LoginForm, RegisterForm
from .now import now
from jeefies.flask_self import protect, render, Login, Logout, get_user
from jeefies import Content, Hexsec

req = request
conpath = os.path.dirname(os.path.dirname(__file__))

@main.route('/')
def index():
    t = now()
    return render('greet.html', tm = t)

@main.route('/login', methods=['GET', "POST"])
def login():
    form = LoginForm()
    t = now()

    if form.validate_on_submit():
        con = Content(conpath, 'user')
        user_name = form.name.data
        #print(user_name, con.has(user_name))
        user = con.get(user_name)
        
        if user is None:
            flash('No such user')
            return redirect(url_for('.login'))

        inpw = form.password.data
        if not Hexsec.decrypt(user[1][0]) == inpw :
            #print(Hexsec.decrypt(user[1][0]))
            flash('Error Password, please try again')
            return redirect(url_for('.login'))

        return Login(redirect('/'), user[0], form.password.data)

    return render('ask_name.html', form=form, tm = t, name=session.get(req.remote_addr, None))

def director():
    flash('You must be logined, click the button on the left side on the top to login')
    return redirect(url_for('.index'))

@main.route('/logout', methods=['GET','POST'])
@protect(director, conpath)
def logout():
    form = LogoutForm()
    if form.sure.data:
        return Logout(redirect("/"))
    return render('logingout.html', name=session.get(req.remote_addr), form=form)

@main.route('/regist', methods=['GET','POST'])
def registor():
    form = RegisterForm()
    if form.validate_on_submit():
        con = Content(conpath, 'user')
        if con.has(form.username.data):
            flash('User name is userd, please change a name')
            return redirect(url_for('.registor'))
        passwords = Content(conpath, 'passwd').all()
        for password in passwords:
            passwd = password[0]
            if  passwd == form.regist_passwd.data:
                break
        else:
            flash('Please enter the right regist password or ask author for help')
            return redirect(url_for('.registor'))
        con.add(form.username.data, [Hexsec.encrypt(form.password.data)])
        flash('You can login now')
        return redirect(url_for('.login'))
    return render('regist.html', form=form, name=session.get(req.remote_addr))

@main.route('/check')
@protect(director,conpath)
def testing():
    return render('base.html', pkgs={'aa':'aa'}, dirs={'bb': 'bb'}, args=[req.remote_addr, req.cookies])
