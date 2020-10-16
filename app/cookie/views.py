from .forms import TestForm
from . import cookie
from flask import url_for, Flask, render_template, redirect, session, flash, request
from flask import make_response as mkresp
from jeefies.flask_self import get_user

import os
basedir = os.path.split(os.path.dirname(__file__))[0]

req = request


@cookie.route('/form', methods=['GET', 'POST'])
def forms():
    form = TestForm()
    if form.validate_on_submit():
        print(form.area.data, type(form.area.data))
    return render_template('test/form.html', form=form)


@cookie.route('/')
def index():
    return "<li><a href='{}'>set</a></li><li><a href='{}'>get</a></li><li><a href='{}'>del</a></li>".format(
        url_for('.setc'), url_for('.getc'), url_for('.delc'))


@cookie.route('/getuser')
def getuser():
    name = get_user(basedir)
    return "<h1>{}</h1>".format(name)


@cookie.route('/set')
def setc():
    resp = mkresp('<h1>Setted</h1>')
    resp.set_cookie('cookie', b'123')
    return resp


@cookie.route('/get')
def getc():
    req = request
    cook = req.cookies.get('cookie')
    cookiess = req.cookies
    return "<h1>{}</h1><p>{}</p>".format(cook, cookiess)


@cookie.route('/del')
def delc():
    resp = mkresp('delete_cookie')
    resp.delete_cookie('cookie')
    return resp


@cookie.route('/delall')
def delall():
    resp = mkresp('delete all cookie')
    d = resp.delete_cookie
    d('name' + req.remote_addr)
    d('passwd'+req.remote_addr)
    d('cookie')
    return resp


@cookie.route('/resp')
def respe():
    resp = mkresp(render_template('base.html', args=[
                  'Ok'], pkgs={1: 1, 2: 2}, dirs={'3': '6'}))
    return resp
