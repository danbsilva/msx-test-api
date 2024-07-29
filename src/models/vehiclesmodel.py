import os, base64, pytz
from datetime import datetime
from uuid import uuid4

from sqlalchemy import text, or_, cast, String
from src.extensions.flask_sqlalchemy import db

timezone = pytz.timezone(os.getenv('TIMEZONE'))


class VehicleModel(db.Model):

    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True, index=True, comment='Identification ID of the vehicle')
    chassi = db.Column(db.String, nullable=False, comment='Chassi of the vehicle')
    renavam = db.Column(db.String, nullable=False, comment='Renavam of the vehicle')
    plate = db.Column(db.String, nullable=False, comment='Plate of the vehicle')
    brand = db.Column(db.String, nullable=False, comment='Brand of the vehicle')
    model = db.Column(db.String, nullable=False, comment='Model of the vehicle')
    year = db.Column(db.String, nullable=False, comment='Year of the vehicle')
    color = db.Column(db.String, nullable=False, comment='Color of the vehicle')
    price = db.Column(db.Float, nullable=False, comment='Price of the vehicle')
    connected = db.Column(db.Boolean, nullable=False, default=False, comment='Connection status of the vehicle')
    created_at = db.Column(db.DateTime, nullable=False, comment='Creation date of the vehicle')
    updated_at = db.Column(db.DateTime, nullable=False, comment='Update date of the vehicle')

    def to_json(self):
        """
        :description: Function to serialize the vehicle object
        :return: dict
        """
        return {
            'id': self.id,
            'chassi': self.chassi,
            'renavam': self.renavam,
            'plate': self.plate,
            'model': self.model,
            'brand': self.brand,
            'year': self.year,
            'color': self.color,
            'price': self.price,
            'connected': self.connected,
        }

    @staticmethod
    def create(data):
        """
        :description: Function to create a new vehicle
        :param data: dict
        :return: VehicleModel or Exception
        """
        try:
            vehicle = VehicleModel(**data)
            vehicle.created_at = datetime.now(timezone)
            vehicle.updated_at = datetime.now(timezone)

            db.session.add(vehicle)
            db.session.commit()

            return vehicle
        except Exception as e:
            db.session.rollback()
            raise e


    @staticmethod
    def update(vehicle, data):
        """
        :description: Function to update a vehicle
        :param vehicle: VehicleModel
        :param data: dict
        :return: VehicleModel or Exception
        """
        try:
            for key, value in data.items():
                setattr(vehicle, key, value)

            vehicle.updated_at = datetime.now(timezone)
            db.session.commit()

            return vehicle
        except Exception as e:
            db.session.rollback()
            raise e


    @staticmethod
    def delete(vehicle):
        """
        :description: Function to delete a vehicle
        :param vehicle: VehicleModel
        :return: True or Exception
        """
        try:
            db.session.delete(vehicle)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e


    @staticmethod
    def get_all(search, page, per_page, offset):
        """
        :description: Function to get all vehicles
        :param search: str
        :param page: int
        :param per_page: int
        :param offset: int
        :return: list of VehicleModel
        """
        query = VehicleModel.query

        if search:
            query = query.filter(
                or_(
                    VehicleModel.model.ilike(f'%{search}%'),
                    VehicleModel.brand.ilike(f'%{search}%'),
                    VehicleModel.year.ilike(f'%{search}%')
                )
            )

        total = query.count()
        query = query.order_by(VehicleModel.id.desc()).limit(per_page).offset(offset)
        return query.all(), total


    @staticmethod
    def get_by_id(id):
        """
        :description: Function to get a vehicle by id
        :param id: int
        :return: VehicleModel or None
        """
        return VehicleModel.query.filter_by(id=id).first()