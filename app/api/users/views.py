from flask import jsonify, request
from bcrypt import hashpw,gensalt,checkpw
from flask_jwt_extended import   create_access_token
from app.models import User
from app.api.users import user_bp
from  app.models import db
from sqlalchemy import or_

# register user
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

# login user
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

# get one user
@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.filter(User.id==user_id).first()
    if user:
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({'message': 'User not found'}), 404


# update user
@user_bp.route('/<int:user_id>',methods = ['PUT'])
def update_user(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    data = request.get_json()
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password = hashpw(data['password'].encode('utf-8'), gensalt())  # Hash the new password
    if 'username' in data:
        user.username = data['username']
    if 'contact' in data:
        user.contact = data['contact']
    if 'address' in data:
        user.address = data['address']
    if 'role' in data:
        user.role = data['role'] 
    if 'verified' in data:
        user.verified = data['verified']
    db.session.commit()

    return jsonify({'message': 'User updated successfully'}), 200

# delete user
@user_bp.route('/<int:user_id>',methods=['DELETE'])
def delete_user(user_id):
    print(user_id)
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 204


# get all users
@user_bp.route('/',methods = ['GET'])
def all_users():
    users = User.query.all()
    if not users:
        return jsonify({'message': 'No users found'}), 404
    return jsonify([user.to_dict() for user in users]), 200