from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.models import Vehicle,Vehicle_specs
from . import vehicle_bp
from app import db

# get all vehicles
@vehicle_bp.route('/',methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    print(vehicles[0])
    if not vehicles:
        return jsonify({'message': 'No vehicles found'}), 404

    return jsonify({'vehicles': [vehicle.get_with_specs() for vehicle in vehicles]}), 200

# get one vehicle
@vehicle_bp.route('/<int:vehicle_id>',methods=['GET'])
def get_one_vehicle(vehicle_id):
    vehicle = Vehicle.query.filter_by(id=vehicle_id).first()
    if vehicle:
        return jsonify(vehicle.get_with_specs()), 200
    return jsonify({'message': 'Vehicle not found'})


# delete a vehicle
@vehicle_bp.route('/<int:vehicle_id>', methods=['DELETE'])
@jwt_required()
def delete_vehicle(vehicle_id):
    verified_user = get_jwt_identity()
    if verified_user['role']!= 'admin':
        return jsonify({'message': 'Unauthorized access'}), 401
    vehicle = Vehicle.query.filter_by(id=vehicle_id).first()
    if vehicle:
        db.session.delete(vehicle)
        db.session.commit()
        return jsonify({'message': 'Vehicle deleted'}), 200
    return jsonify({'message': 'Vehicle not found'}), 

#create a new vehicle
@vehicle_bp.route('/', methods=['POST'])
@jwt_required()
def new_vehicle():
    verified_user = get_jwt_identity()
    if verified_user['role']!= 'admin':
        return jsonify({'message': 'Unauthorized access'}), 401
    try:
        data = request.get_json()
        new_vehicle = Vehicle(rental_rate=data['rental_rate'])
        vehicle_specs = Vehicle_specs(
        manufacturer="Toyota",
        model="Corolla",
        year=2020,
        engine_capacity=1800,
        transmission_capacity=6,
        seating_capacity=5,
        color="Blue",
        features="Airbags, ABS",
        fuel_type="Petrol",
        vehicle=new_vehicle
        )
        db.session.add(new_vehicle)
        db.session.add(vehicle_specs)
        db.session.commit()
        return jsonify({'message': new_vehicle.get_with_specs()}), 201
    except Exception as e:
        db.session.rollback() 
        return jsonify({'error': str(e)}), 400  # 


# update the vehicle
@vehicle_bp.route('/<int:vehicle_id>', methods=['PUT'])
@jwt_required()
def update_vehicle(vehicle_id):
    verified_user = get_jwt_identity()
    if verified_user['role']!= 'admin':
        return jsonify({'message': 'Unauthorized access'}), 401
    data = request.get_json()
    vehicle = Vehicle.query.filter_by(id=vehicle_id).first()
    if vehicle:
        vehicle.update(**data)
        db.session.commit()
        return jsonify({'message': vehicle.get_with_specs()}), 200
    return jsonify({'message': 'Vehicle not found'}), 404