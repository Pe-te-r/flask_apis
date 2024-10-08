from sqlalchemy import ForeignKey
from sqlalchemy.orm import  relationship
from random import randint
import enum
from datetime import datetime,timezone
from . import db

class RoleEnum(enum.Enum):
    ADMIN = 'admin'
    USER = 'user'

class SubjectEnum(enum.Enum):
    COMPLAIN = 'complain'
    SUGGESTION = 'suggestion'
    QUESTION = 'question'
    OTHER = 'other'

class StatusEnum(enum.Enum):
    PENDING = 'pending'
    RESOLVED = 'resolved'

class FleetEnum(enum.Enum):
    DONE = 'done'
    IN_PROGRESS = 'in_progress'

class BookEnum(enum.Enum):
    TAKEN = 'token'
    RETURNED = 'returned'
    LOST = 'lost'
    WAITTING = 'waiting'

    

class Code(db.Model):
    id = db.Column(db.Integer, ForeignKey('user.id'), primary_key=True)
    code = db.Column(db.String(4), nullable=False,default=str(randint(000,9999)).zfill(4))

    # relationship
    user = relationship('User',uselist=False,back_populates='code')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    username=db.Column(db.String(255), nullable=False,unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contact = db.Column(db.String(15), nullable=True)
    address = db.Column(db.String(40), nullable=True)
    role = db.Column(db.Enum(RoleEnum),nullable=False,default=RoleEnum.USER)
    verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime,nullable=False,default=datetime.now(timezone.utc))

    # relationship
    code = relationship('Code',uselist=False,back_populates='user')
    support = relationship('Customer_support',back_populates='user')
    booking = relationship('Booking',back_populates='user')

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'contact': self.contact,
            'address': self.address,
            'role': self.role.name,
            # 'created_at': self.created_at.isoformat(),
        }

    def set_code(self):
        code = Code(id=self.id)
        db.session.add(code)
        db.session.commit()
    
    def update_code(self):
        code = Code.query.filter_by(id=self.id).first()
        if code:
            code.code = str(randint(000,9999)).zfill(4)
            db.session.commit()
        else:
            self.set_code()

    def get_code(self):
        code = Code.query.filter_by(id=self.id).first()
        if code:
            return code.code
        else:
            return None

    def is_verified(self):
        return self.verified
    
    def verify_code(self, code):
        return self.code.code == code
    


class Customer_support(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.Enum(SubjectEnum),nullable=False,default=SubjectEnum.COMPLAIN)
    description = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Enum(StatusEnum), nullable=False, default=StatusEnum.PENDING)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    # relationship
    user = relationship('User',back_populates='support',uselist=False)


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rental_rate = db.Column(db.Float,nullable=False)

    # relationship
    fleet = relationship('Fleet',back_populates='vehicle')
    specs = relationship('Vehicle_specs',uselist=False,back_populates='vehicle')
    booking = relationship('Booking',back_populates='vehicle')

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            elif self.specs and hasattr(self.specs, key):
                self.specs.update(key, value)  # Call update method in Vehicle_specs
            else:
                raise AttributeError(f"{key} is not a valid attribute of Vehicle or Vehicle_specs")

        db.session.commit()  # Commit the changes after all updates

    def get_with_specs(self):
        if not self.specs:
            return None
        
        print(self.specs)
        return {
           'rental_rate': self.rental_rate,
           'specs': self.specs.to_dict()
        }


class Fleet(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vehicle_id = db.Column(db.Integer, ForeignKey('vehicle.id'), nullable=False) 
    taken_date = db.Column(db.DateTime,nullable=True)
    return_date = db.Column(db.DateTime,nullable=True)
    current_value = db.Column(db.Float,nullable=True)
    maintance_cost = db.Column(db.Float,nullable=True)
    status = db.Column(db.Enum(FleetEnum),nullable=False,default=FleetEnum.DONE)

    # relationship
    vehicle = relationship('Vehicle',back_populates='fleet')


class Vehicle_specs(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vehicle_id = db.Column(db.Integer, ForeignKey('vehicle.id'), nullable=False)
    manufacturer = db.Column(db.String(255), nullable=False)
    model = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    engine_capacity = db.Column(db.Integer, nullable=False)
    transmission_capacity = db.Column(db.Integer, nullable=False)
    seating_capacity = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(100), nullable=False)
    features = db.Column(db.String(255), nullable=False)
    fuel_type = db.Column(db.String(100), nullable=False)

    # relationship
    vehicle= relationship('Vehicle',back_populates='specs',uselist=False)

    def update(self, key, value):
        """Update the attribute of the vehicle specs."""
        if hasattr(self, key):
            setattr(self, key, value)
            db.session.commit()
        else:
            raise AttributeError(f"{key} is not a valid attribute of Vehicle_specs")
    

    def to_dict(self):
        return {
           'manufacturer': self.manufacturer,
           'model': self.model,
           'year': self.year,
           'engine_capacity': self.engine_capacity,
           'transmission_capacity': self.transmission_capacity,
          'seating_capacity': self.seating_capacity,
           'color': self.color,
           'features': self.features,
           'fuel_type': self.fuel_type
        }



class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    created_at = db.Column(db.DateTime,nullable=False,default=datetime.now(timezone.utc))

    # relationship
    booking = relationship('Booking',back_populates='location')

    def to_dict(self):
        return {
            'id':self.id,
            'name': self.name,
            'address': self.address,
            'contact': self.contact,
        }

    def update(self,**kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"{key} is not a valid attribute of Location")

        db.session.commit()

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer,ForeignKey('user.id'),nullable=False)
    vehicle_id = db.Column(db.Integer, ForeignKey('vehicle.id'), nullable=False)
    Location_id = db.Column(db.Integer, ForeignKey('location.id'),nullable=False)
    booking_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum(BookEnum), nullable=False,default=BookEnum.WAITTING)
    created_at = db.Column(db.DateTime,nullable=False,default=datetime.now(timezone.utc))

    # relationship
    user = relationship('User',back_populates='booking')
    vehicle= relationship('Vehicle',back_populates='booking')
    location = relationship('Location',back_populates='booking')
