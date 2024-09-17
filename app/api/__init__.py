from app.api.vehicles import vehicle_bp
from app.api.post import post_bp
from app.api.users import user_bp

def register_bp(app):
   app.register_blueprint(vehicle_bp,url_prefix='/vehicle')
   app.register_blueprint(post_bp,url_prefix='/posts')
   app.register_blueprint(user_bp,url_prefix='/users')