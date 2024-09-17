from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from dotenv import load_dotenv
from app.models import db
from app.api import register_bp
from .config import Config

load_dotenv()

jwt= JWTManager()
mg= Migrate()
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    mail.init_app(app)

    # Migrate(app, db)
    # JWTManager(app)
    jwt.init_app(app)
    mg.init_app(app,db)

    register_bp(app)
    return app