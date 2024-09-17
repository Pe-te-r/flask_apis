from flask import  request, jsonify
from app import db
from app.models.models import Location
from app.api.location import location_bp

@location_bp.route('/',methods=['GET'])
def get_locations():
    locations = Location.query.all()
    if not locations:
        return jsonify({'message': 'No locations found'}), 404
    return {'locations': [location.to_dict() for location in locations]}, 200


@location_bp.route('/<int:location_id>')
def get_one_location_bp(location_id):
    location = Location.query.filter_by(id=location_id).first()
    if location:
        return jsonify(location.to_dict()), 200
    return jsonify({'message': 'Location not found'}), 404

@location_bp.route('/<int:location_id>', methods=['PUT'])
def update_location(location_id):
    data = request.get_json()
    location = Location.query.filter_by(id=location_id).first()
    if location:
        location.update(**data)
        return jsonify({'message': 'Location updated successfully'}), 200
    return jsonify({'message': 'Location not found'}), 404


@location_bp.route('/<int:location_id>',methods=['DELETE'])
def delete_location(location_id):
    location = Location.query.filter_by(id=location_id).first()
    if location:
        db.session.delete(location)
        db.session.commit()
        return jsonify({'message': 'Location deleted successfully'}), 200