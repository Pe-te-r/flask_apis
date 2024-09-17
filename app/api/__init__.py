from app.api.vehicles import vehicle_bp
from app.api.location import location_bp
from app.api.users import user_bp

def register_bp(app):
   app.register_blueprint(user_bp,url_prefix='/users')
   app.register_blueprint(location_bp,url_prefix='/locations')
   app.register_blueprint(vehicle_bp,url_prefix='/vehicle')