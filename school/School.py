import os
import glob
import sys
import time
import datetime

from flask import Flask, redirect, url_for, render_template
from flask import flash, session
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
"""init for the data's path"""
basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)

"""init the flask app"""
app = Flask(__name__)
app.config['SECRET_KEY'] = "password"

bootstrap = Bootstrap(app)
moment = Moment(app)

"""init the wtform"""
class UserForm(FlaskForm):
    user = StringField('What is your name?')
    submit = SubmitField('Submit')

@app.route('/')
def index():
    t = time.localtime()
    timedict = {
            'year': t.tm_year,
            'month': t.tm_mon,
            'day': t.tm_mday,
            'hour': t.tm_hour,
            'mi' : t.tm_min,
            'sec' : t.tm_sec,
            'fday': t.tm_yday,
            'wday': t.tm_wday + 1
            }
    di = {1:'Monday', 2:'Tuesday', 3:'Wednesday', 4:'Thursday', 5:'Friday', 6:'Saturday', 7:'Sunday'}
    timedict['wday'] = di[t.tm_wday + 1]
    return render_template("index.html", **timedict)

@app.route('/study')
def study_base():
    staticpath = os.path.join(basedir,'static', 'study')
    dirs = {}
    pkgs = {}
    for root,paths,files in os.walk(staticpath):
        for file in files:
            pkgs[file] = url_for('downloadfile', filename=file, _external=True)
        for path in paths:
            dirs[path] = url_for('study_base', _external=True) + f'/{path}'
    print(dirs,pkgs)
    return render_template('study.html', dirs = dirs, pkgs=pkgs, upperpath = url_for('index'))
            
@app.route('/study/<path:filename>')
def study_upper(filename):
    staticpath = os.path.join(basedir,'static','study', filename)
    pkgs = {}; dirs = {}
    if not '/' in filename:
        upper = url_for('study_base', _external=True)
    else:
        upper = url_for('study_base', _external=True) + ''.join(filename.split('/')[:-1])
    for root, files, paths in os.walk(staticpath):
        for file in files:
            pkgs[file] = url_for('download', _external=True) + f'/{filename}/{file}'
        for path in paths:
            dirs[path] = url_for('study_base', _external=True) + f'/{filename}/{path}'
    return render_template('study.html', pkgs=pkgs, dirs=dirs, upperpath = upper)


@app.route('/downloading/<path:filename>')
def downloadfile(filename):
    path = url_for('static', filename=f'study/{filename}', _external=True)
    return redirect(path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

