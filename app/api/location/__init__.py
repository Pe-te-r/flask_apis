from flask import Blueprint

location_bp = Blueprint('locations',__name__)

from .views import *  # noqa: E402, F403
