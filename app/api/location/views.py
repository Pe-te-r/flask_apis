from flask import  request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.models import Location
from app.api.location import location_bp

@location_bp.route('/',methods=['GET'])
def get_locations():
    locations = Location.query.all()
    if not locations:
        return jsonify({'message': 'No locations found'}), 404
    return {'locations': [location.to_dict() for location in locations]}, 200


@location_bp.route('/<int:location_id>',methods=['GET'])
def get_one_location_bp(location_id):
    location = Location.query.filter_by(id=location_id).first()
    if location:
        return jsonify(location.to_dict()), 200
    return jsonify({'message': 'Location not found'}), 404

@location_bp.route('/<int:location_id>', methods=['PUT'])
@jwt_required()
def update_location(location_id):
    verified_user = get_jwt_identity()
    if verified_user['role'] != 'admin':
        return jsonify({'message': 'Unauthorized access'}), 401
    data = request.get_json()
    location = Location.query.filter_by(id=location_id).first()
    if location:
        location.update(**data)
        return jsonify({'message': 'Location updated successfully'}), 200
    return jsonify({'message': 'Location not found'}), 404


@location_bp.route('/<int:location_id>',methods=['DELETE'])
@jwt_required()
def delete_location(location_id):
    verified_user = get_jwt_identity()
    if verified_user['role']!= 'admin':
        return jsonify({'message': 'Unauthorized access'}), 401
    location = Location.query.filter_by(id=location_id).first()
    if location:
        db.session.delete(location)
        db.session.commit()
        return jsonify({'message': 'Location deleted successfully'}), 200


@location_bp.route('/',methods =['POST'])
@jwt_required()
def create_location():
    verified_user = get_jwt_identity()
    if verified_user['role'] != 'admin':
        return jsonify({'message': 'Unauthorized access'}), 401
    data = request.get_json()
    location = Location(name=data['name'],address=data['address'],contact=data['contact'])
    db.session.add(location)
    db.session.commit()
    return jsonify({'message': 'Location created successfully', 'location_id': location.id}), 201