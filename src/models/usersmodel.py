import os, pytz
from datetime import datetime

from sqlalchemy import text, or_, cast, String
from werkzeug.security import check_password_hash, generate_password_hash

from src.extensions.flask_sqlalchemy import db

timezone = pytz.timezone(os.getenv('TIMEZONE'))


class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, index=True, comment='Identification ID of the user')
    name = db.Column(db.String, nullable=False, comment='Name of the user')
    email = db.Column(db.String, nullable=False, unique=True, comment='Email of the user')
    password = db.Column(db.String, nullable=False, comment='Password of the user')
    active = db.Column(db.Boolean, nullable=False, default=True, comment='Status of the user')
    created_at = db.Column(db.DateTime, nullable=False, comment='Creation date of the vehicle')
    updated_at = db.Column(db.DateTime, nullable=False, comment='Update date of the vehicle')

    def to_json(self):
        """
        :description: Function to serialize the vehicle object
        :return: dict
        """
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'active': self.active,
        }

    @staticmethod
    def create(data):
        """
        :description: Function to create a new user
        :param data: dict
        :return: UserModel or Exception
        """
        try:
            user = UserModel(**data)
            user.created_at = datetime.now(timezone)
            user.updated_at = datetime.now(timezone)

            db.session.add(user)
            db.session.commit()

            return user
        except Exception as e:
            db.session.rollback()
            raise e


    @staticmethod
    def update(user, data):
        """
        :description: Function to update a user
        :param user: UserModel
        :param data: dict
        :return: UserModel or Exception
        """
        try:
            for key, value in data.items():
                setattr(user, key, value)

            user.updated_at = datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')
            db.session.commit()

            return user
        except Exception as e:
            db.session.rollback()
            raise e


    @staticmethod
    def delete(user):
        """
        :description: Function to delete a user
        :param vehicle: UserModel
        :return: True or Exception
        """
        try:
            db.session.delete(user)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e


    @staticmethod
    def encrypt_password(password):
        """
        :description: Function to encrypt the password
        :param password: string
        :return: hash string
        """
        return generate_password_hash(password)


    @staticmethod
    def check_password(hashed_password, password):
        """
        :description: Function to check the password
        :param hashed_password: hash string
        :param password: string
        :return: boolean
        """
        return check_password_hash(hashed_password, password)


    @staticmethod
    def get_by_email(email):
        """
        :description: Function to get user by email
        :param email: string
        :return: UserModel or None
        """
        return UserModel.query.filter_by(email=email).first()