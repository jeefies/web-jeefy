from flask import render_template
from . import main

@main.errorhandler(404)
def page_not_found(e):
    return render_template('4040.html'), 404

@main.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
