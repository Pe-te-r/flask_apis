from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from app.models import db
from app.api import register_bp
from .config import Config

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    migrate = Migrate(app, db)
    jwt = JWTManager(app)

    register_bp(app)
    return app