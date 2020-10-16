from flask import Blueprint

cookie = Blueprint('cookie', __name__)

from . import views
