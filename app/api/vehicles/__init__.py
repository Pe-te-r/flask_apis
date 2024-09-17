from flask import  Blueprint

vehicle_bp = Blueprint('vehicles', __name__)


from .views import *  # noqa: E402, F403

