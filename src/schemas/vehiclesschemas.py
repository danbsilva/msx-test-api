import re
from marshmallow import Schema, fields, validate, ValidationError
from marshmallow.fields import Nested


#### VEHICLES ####
class VehiclePostSchema(Schema):
    chassi = fields.String(
        required=True,
        error_messages={
            'required': 'The chassi is required'
        }
    )
    renavam = fields.String(
        required=True,
        error_messages={
            'required': 'The renavam is required'
        }
    )
    plate = fields.String(
        required=True,
        error_messages={
            'required': 'The plate is required'
        }
    )
    brand = fields.String(
        required=True,
        error_messages={
            'required': 'The brand is required'
        }
    )
    model = fields.String(
        required=True,
        error_messages={
            'required': 'The model is required'
        }
    )
    year = fields.Integer(
        required=True,
        error_messages={
            'required': 'The year is required'
        }
    )
    color = fields.String(
        required=True,
        error_messages={
            'required': 'The color is required'
        }
    )
    price = fields.Float(
        required=True,
        error_messages={
            'required': 'The price is required'
        }
    )
    connected = fields.Boolean(
        required=True,
        error_messages={
            'required': 'The connected is required'
        }
    )

    class Meta:
        ordered = True

class VehicleGetSchema(Schema):
    id = fields.Integer(required=True)
    chassi = fields.String(required=True)
    renavam = fields.String(required=True)
    plate = fields.String(required=True)
    brand = fields.String(required=True)
    model = fields.String(required=True)
    year = fields.Integer(required=True)
    color = fields.String(required=True)
    price = fields.Float(required=True)
    connected = fields.Boolean(required=True)

    class Meta:
        ordered = True

class VehiclePatchSchema(Schema):
    chassi = fields.String(
        required=False,
    )
    renavam = fields.String(
        required=False,
    )
    plate = fields.String(
        required=False,
    )
    brand = fields.String(
        required=False,
    )
    model = fields.String(
        required=False,
    )
    year = fields.Integer(
        required=False,
    )
    color = fields.String(
        required=False,
    )
    price = fields.Float(
        required=False,
    )
    connected = fields.Boolean(
        required=False,
    )

    class Meta:
        ordered = True
