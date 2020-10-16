from flask import Blueprint

study = Blueprint('study', __name__)

from . import views
