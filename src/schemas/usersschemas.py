import re
from marshmallow import Schema, fields, validate, ValidationError
from marshmallow.fields import Nested


#### USERS ####
class UserPostSchema(Schema):
    name = fields.String(
        required=True,
        error_messages={
            'required': 'The name is required'
        }
    )
    email = fields.Email(
        required=True,
        error_messages={
            'required': 'The email is required',
            'invalid': 'The email is invalid'
        }
    )
    password = fields.String(
        required=True,
        error_messages={
            'required': 'The password is required'
        },
        validate=[
            validate.Length(
                min=6,
                max=12,
                error='The password must be between 6 and 12 characters'
            )
        ]
    )

    class Meta:
        ordered = True

class UserGetSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    email = fields.Email(required=True)
    active = fields.Boolean(required=True)

    class Meta:
        ordered = True

class UserPatchSchema(Schema):
    name = fields.String(
        required=False,
    )
    email = fields.Email(
        required=False,
    )
    active = fields.Boolean(
        required=False,
    )

    class Meta:
        ordered = True


class UserLoginSchema(Schema):
    email = fields.Email(
        required=True,
        error_messages={
            'required': 'The email is required',
            'invalid': 'The email is invalid'
        }
    )
    password = fields.String(
        required=True,
        error_messages={
            'required': 'The password is required'
        }
    )

    class Meta:
        ordered = True


class UserLoginResponseSchema(Schema):
    access_token = fields.String(required=True)

    class Meta:
        ordered = True