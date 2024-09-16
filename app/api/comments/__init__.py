from flask import  Blueprint

comment_bp = Blueprint('comments', __name__)


from .views import *  # noqa: E402, F403

