from flask import Blueprint
import hy

user = Blueprint('user', __name__)

from . import views
from . import accviews
