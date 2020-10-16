import os
import glob

from . import study
from flask import url_for, Flask, render_template, redirect, session, flash, request
from flask import make_response as mkresp
from jeefies.flask_self import protect, render, walker
req = request


def errors():
    flash('You must be logined!')
    return redirect(url_for('.advice'))


base = os.path.abspath(os.path.dirname(__file__))
conpath = os.path.dirname(base)
basedir = os.path.join(os.path.split(base)[0], 'static', 'study')


@study.route('/')
@protect(errors, conpath)
def index():
    paths, files = walker(basedir)
    pkgs = {}
    dirs = {'../': url_for('main.index')}
    if 1:
        for file in files:
            pkgs[file] = url_for('.downloading', filename=file)
        for p in paths:
            dirs[p + '/'] = url_for('.studies', direct=p)
    return render('study/index.html', pkgs=pkgs, dirs=dirs)


@study.route('/<path:direct>')
@protect(errors, conpath)
def studies(direct):
    base = os.path.join(basedir, direct)
    upper = os.path.split(direct)[0]
    if upper == '':
        upper = url_for("study.index", _external=True)
        print("index")
    try:
        paths, files = walker(base)
    except:
        print("error walk")
    pkgs = {}
    dirs = {'../': upper}
    if 1:
        for file in files:
            pkgs[file] = url_for(
                '.downloading', filename=os.path.join(direct, file))
        for p in paths:
            dirs[p] = url_for('.studies', direct=os.path.join(base, p))
    return render('study/index.html', pkgs=pkgs, dirs=dirs)


@study.route('/download/<path:filename>')
@protect(errors, conpath)
def downloading(filename):
    path = url_for('static', filename='study/' + filename)
    return redirect(path)


@study.route('/advice')
def advice():
    baseurl = url_for('main.index', _external=True)
    url = baseurl[:-1] + ':5000'
    return render_template('study/advice.html', school_url=url)
