from flask import jsonify, request
from bcrypt import hashpw,gensalt,checkpw
from flask_jwt_extended import jwt_required,  create_access_token
from app.models import User
from app.api.users import user_bp
from  app.models import db
from sqlalchemy import or_

@user_bp.route('/register',methods=['POST'])
def register_user():
    data = request.get_json()
    user_exists =User.query.filter(or_(User.name == data['name'], User.email == data['email'])).first()
    if user_exists:
        return jsonify({'message': 'User already exists'}), 409

    password = hashpw(data['password'].encode('utf-8'),gensalt())
    user = User(name=data['name'], email = data['email'],contact = data['contact'],address=data['address'],username=data['username'],password=password.decode('utf-8') )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': user.to_dict()}), 201


@user_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user:
        hashed_password = user.password.encode('utf-8')  # Ensure the stored password is in bytes
        input_password = data['password'].encode('utf-8')  # Convert input password to bytes
        
        if checkpw(input_password, hashed_password):
            access_token = create_access_token(identity=user.id)
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    else:
        return jsonify({'message': 'User not found'}), 404
    
@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.filter(User.id==user_id).first()
    if user:
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({'message': 'User not found'}), 404



@user_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    pass