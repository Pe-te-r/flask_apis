from flask import Blueprint

post_bp = Blueprint('posts',__name__)

from .views import *  # noqa: E402, F403
