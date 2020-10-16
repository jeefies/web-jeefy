from flask import Blueprint

roomy = Blueprint('roomy', __name__)

from . import views
