import os

from flask import request, jsonify
from flask_restful import Resource
from flask_paginate import Pagination

from flask_jwt_extended import jwt_required

from marshmallow import ValidationError
from werkzeug.exceptions import UnsupportedMediaType

from src.schemas import vehiclesschemas
from src.models.vehiclesmodel import VehicleModel

from src import controllers

## VEHICLES ##
class VehiclesResource(Resource):
    @staticmethod
    @jwt_required()
    def post():
        """
        :description: Create a new vehicle
        :param data: JSON object with vehicle data
        :return: JSON object with vehicle data created
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

            schema_validate = controllers.validate_schema(schema=vehiclesschemas.VehiclePostSchema(), payload=data)
            if schema_validate:
                return {'message': schema_validate}, 400

            try:
                vehicle = VehicleModel.create(data=data)
            except Exception as e:
                return {'message': 'Error creating vehicle'}, 400

            schema = vehiclesschemas.VehicleGetSchema()
            schema_data = schema.dump(vehicle)

            return {'vehicle': schema_data}, 201

        except Exception as e:
            return {'message': 'Internal Server Error'}, 500

    @staticmethod
    @jwt_required()
    def get():
        """
        :description: Get all vehicles
        :param search: search string
        :param page: page number
        :param per_page: number of items per page
        :param offset: offset for pagination
        :return: JSON object with vehicles data
        """
        try:
            search = request.args.get('search', '', type=str)
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            offset = (page - 1) * per_page

            vehicles, total = VehicleModel.get_all(search=search, page=page, per_page=per_page, offset=offset)

            pagination = Pagination(page=page, per_page=per_page, total=total)

            schema = vehiclesschemas.VehicleGetSchema(many=True)
            schema_data = schema.dump(vehicles)

            return {'vehicles': schema_data,
                    'pagination': {
                        'total_pages': pagination.total_pages,
                        'current_page': page,
                        'per_page': pagination.per_page,
                        'total_items': pagination.total,
                        'has_next': pagination.has_next,
                        'has_prev': pagination.has_prev,
                        'total_items_this_page': len(vehicles),
                        'offset': offset
                    }}, 200

        except Exception as e:
            return {'message': 'Internal Server Error'}, 500



## VEHICLE ##
class VehicleResource(Resource):
    @staticmethod
    @jwt_required()
    def get(id):
        """
        :description: Get vehicle by id
        :param id: vehicle id
        :return: JSON object with vehicle data
        """
        try:
            vehicle = VehicleModel.get_by_id(id=id)
            if not vehicle:
                return {'message': 'Vehicle not found'}, 404

            schema = vehiclesschemas.VehicleGetSchema()
            schema_data = schema.dump(vehicle)

            return {'vehicle': schema_data}, 200

        except Exception as e:
            return {'message': 'Internal Server Error'}, 500

    @staticmethod
    @jwt_required()
    def patch(id):
        """
        :description: Update vehicle by id
        :param id: vehicle id
        :return: JSON object with vehicle data updated
        """
        try:
            try:
                data = request.get_json()
            except UnsupportedMediaType as e:
                return {'message': 'Unsupported Media Type'}, 415
            except Exception as e:
                return {'message': 'Bad Request'}, 400

            schema_validate = controllers.validate_schema(schema=vehiclesschemas.VehiclePatchSchema(), payload=data)
            if schema_validate:
                return {'message': schema_validate}, 400

            vehicle = VehicleModel.get_by_id(id=id)
            if not vehicle:
                return {'message': 'Vehicle not found'}, 404

            try:
                vehicle = VehicleModel.update(vehicle=vehicle, data=data)
            except Exception as e:
                return {'message': 'Error updating vehicle'}, 400

            schema = vehiclesschemas.VehicleGetSchema()
            schema_data = schema.dump(vehicle)

            return {'vehicle': schema_data}, 200

        except Exception as e:
            return {'message': 'Internal Server Error'}, 500


    @staticmethod
    @jwt_required()
    def delete(id):
        """
        :description: Delete vehicle by id
        :param id: vehicle id
        :return: Empty object
        """
        try:
            vehicle = VehicleModel.get_by_id(id=id)
            if not vehicle:
                return {'message': 'Vehicle not found'}, 404

            try:
                VehicleModel.delete(vehicle=vehicle)
            except Exception as e:
                return {'message': 'Error deleting vehicle'}, 400

            return {}, 204

        except Exception as e:
            return {'message': 'Internal Server Error'}, 500