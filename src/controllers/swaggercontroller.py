import os

from flask import request, make_response, render_template
from flask_restful import Resource
from marshmallow import ValidationError

from src import docs

class SwaggerResource(Resource):
    @staticmethod
    def get():
        try:
            combined_swagger = {
                "swagger": "2.0",
                "info": {
                    "description": "",
                    "version": "1.0.0",
                    "title": "API",

                },
            }
            paths = {}
            paths.update(docs.doc_swagger['paths'])

            definitions = {}
            definitions.update(docs.doc_swagger['definitions'])

            security_definitions = {
                "Authorization": {
                    "type": "apiKey",
                    "name": "Authorization",
                    "in": "header"
                }
            }

            combined_swagger.update({
                "paths": paths,
                "definitions": definitions,
                "securityDefinitions": security_definitions
            })
            return combined_swagger

        except Exception as e:
            return {'message': 'Internal server error'}, 500


class SwaggerUIResource(Resource):
    @staticmethod
    def get():
        try:
            return make_response(render_template('swaggerui.html'))
        except Exception as e:
            return {'message': 'Internal server error'}, 500
