import os

from flask import request, jsonify
from flask_restful import Resource
from flask_paginate import Pagination
from flask_jwt_extended import create_access_token

from marshmallow import ValidationError
from werkzeug.exceptions import UnsupportedMediaType

from src.schemas import usersschemas
from src.models.usersmodel import UserModel

from src import controllers

## USERS ##
class UsersResource(Resource):
    @staticmethod
    def post():
        """
        :description: Create a new user
        :param data: JSON object with user data
        :return: JSON object with user data created
        """
        try:
            try:
                data = request.get_json()
            except UnsupportedMediaType as e:
                return {'message': 'Unsupported Media Type'}, 415
            except Exception as e:
                return {'message': 'Bad Request'}, 400
            except Exception as e:
                return {'message': 'Internal Server Error'}, 500

            schema_validate = controllers.validate_schema(schema=usersschemas.UserPostSchema(), payload=data)
            if schema_validate:
                return {'message': schema_validate}, 400

            if UserModel.get_by_email(email=data.get('email')):
                return {'message': 'User already exists'}, 400

            try:
                data['password'] = UserModel.encrypt_password(password=data.get('password'))
                user = UserModel.create(data=data)
            except Exception as e:
                return {'message': 'Error creating user'}, 400

            schema = usersschemas.UserGetSchema()
            schema_data = schema.dump(user)

            return {'user': schema_data}, 201

        except Exception as e:
            return {'message': 'Internal Server Error'}, 500



## LOGIN ##
class UserLoginResource(Resource):
    @staticmethod
    def post():
        """
        :description: Login user
        :param data: JSON object with email and password
        :return: JSON object with access token
        """
        try:
            try:
                data = request.get_json()
            except UnsupportedMediaType as e:
                return {'message': 'Unsupported Media Type'}, 415
            except Exception as e:
                return {'message': 'Bad Request'}, 400

            schema_validate = controllers.validate_schema(schema=usersschemas.UserLoginSchema(), payload=data)
            if schema_validate:
                return {'message': schema_validate}, 400

            user = UserModel.get_by_email(email=data.get('email'))
            if not user:
                return {'message': 'User not found'}, 404

            if not UserModel.check_password(hashed_password=user.password, password=data.get('password')):
                return {'message': 'Invalid credentials'}, 400

            access_token = create_access_token(identity=user.id)

            schema = usersschemas.UserLoginResponseSchema()
            schema_data = schema.dump({'access_token': access_token})

            return schema_data, 200

        except Exception as e:
            return {'message': 'Internal Server Error'}, 500