from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


from .models import User  # noqa: E402, F401
