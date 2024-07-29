from src.schemas import usersschemas, vehiclesschemas


def return_model_dict(schema):
    schema_attributes = schema.fields
    model_dict = {}

    # Iterar sobre os atributos para obter os nomes dos campos
    for field_name, field_obj in schema_attributes.items():
        model_dict[field_name] = field_obj.__class__.__name__  #

    return model_dict


def convert_to_swagger_dict(schema):
    swagger_dict = {
        "type": "object",
        "properties": {}
    }

    for field_name, field_obj in schema.fields.items():
        field_type = field_obj.__class__.__name__.lower()
        field_format = None

        types = {}
        field_items = {}

        if field_type == "datetime":
            field_type = "string"
            field_format = "date-time"

        elif field_type == "email":
            field_type = "string"
            field_format = "email"

        elif field_type == "dict":
            field_type = "object"

        elif field_type == "list":
            field_type = "array"
            field_items.update({})
            types.update({"items": field_items})

        elif field_type == "nested":
            field_type = "object"
            field_items.update(convert_to_swagger_dict(field_obj.schema))
            types.update(field_items)

        elif field_type == "float":
            field_type = "number"
            field_format = "float"
            types.update({"type": field_type})

        else:
            types.update({"type": field_type})

        if field_format:
            types.update({"format": field_format})

        swagger_dict["properties"][field_name] = types
    return swagger_dict


paths = {
    # Users
    '/api/users/register': {
        'post': {
            'tags': ['users'],
            'summary': 'Register user',
            'description': 'Register user',
            'parameters': [
                {
                    'name': 'body',
                    'in': 'body',
                    'schema': {
                        '$ref': '#/definitions/UserPostSchema'
                    },
                    'required': True,
                    'description': 'User data'
                }
            ],
            'responses': {
                '200': {
                    'description': 'OK',
                    'schema': {
                        '$ref': '#/definitions/UserGetSchema'
                    }
                }
            },
        },
    },
    '/api/users/login': {
        'post': {
            'tags': ['users'],
            'summary': 'Login user',
            'description': 'Login user',
            'parameters': [
                {
                    'name': 'body',
                    'in': 'body',
                    'schema': {
                        '$ref': '#/definitions/UserLoginSchema'
                    },
                    'required': True,
                    'description': 'User login data'
                }
            ],
            'responses': {
                '200': {
                    'description': 'OK',
                    'schema': {
                        '$ref': '#/definitions/UserLoginResponseSchema'
                    }
                }
            }
        }
    },

    # Vehicles
    '/api/vehicles': {
        'post': {
            'tags': ['vehicles'],
            'summary': 'Register vehicle',
            'description': 'Register vehicle',
            'parameters': [
                {
                    'name': 'body',
                    'in': 'body',
                    'schema': {
                        '$ref': '#/definitions/VehiclePostSchema'
                    },
                    'required': True,
                    'description': 'Vehicle data'
                }
            ],
            'responses': {
                '200': {
                    'description': 'OK',
                    'schema': {
                        '$ref': '#/definitions/VehicleGetSchema'
                    }
                }
            },
            'security': [
                {
                    'Authorization': [
                        'users'
                    ]
                }
            ]
        },
        'get': {
            'tags': ['vehicles'],
            'summary': 'Get vehicles',
            'description': 'Get vehicles',
            'responses': {
                '200': {
                    'description': 'OK',
                    'schema': {
                        '$ref': '#/definitions/VehiclesGetSchema'
                    }
                }
            },
            'security': [
                {
                    'Authorization': [
                        'users'
                    ]
                }
            ]
        }
    },
    '/api/vehicles/{id}': {
        'get': {
            'tags': ['vehicles'],
            'summary': 'Get vehicle',
            'description': 'Get vehicle',
            'parameters': [
                {
                    'name': 'id',
                    'in': 'path',
                    'type': 'string',
                    'required': True,
                    'description': 'Vehicle ID'
                }
            ],
            'responses': {
                '200': {
                    'description': 'OK',
                    'schema': {
                        '$ref': '#/definitions/VehicleGetSchema'
                    }
                }
            },
            'security': [
                {
                    'Authorization': [
                        'users'
                    ]
                }
            ]
        },
        'patch': {
            'tags': ['vehicles'],
            'summary': 'Update vehicle',
            'description': 'Update vehicle',
            'parameters': [
                {
                    'name': 'id',
                    'in': 'path',
                    'type': 'string',
                    'required': True,
                    'description': 'Vehicle ID'
                },
                {
                    'name': 'body',
                    'in': 'body',
                    'schema': {
                        '$ref': '#/definitions/VehiclePatchSchema'
                    },
                    'required': True,
                    'description': 'Vehicle data'
                }
            ],
            'responses': {
                '200': {
                    'description': 'OK',
                    'schema': {
                        '$ref': '#/definitions/VehicleGetSchema'
                    }
                }
            },
            'security': [
                {
                    'Authorization': [
                        'users'
                    ]
                }
            ]
        },
        'delete': {
            'tags': ['vehicles'],
            'summary': 'Delete vehicle',
            'description': 'Delete vehicle',
            'parameters': [
                {
                    'name': 'id',
                    'in': 'path',
                    'type': 'string',
                    'required': True,
                    'description': 'Vehicle ID'
                }
            ],
            'responses': {
                '200': {
                    'description': 'OK',
                    'schema': {
                        '$ref': '#/definitions/VehicleGetSchema'
                    }
                }
            },
            'security': [
                {
                    'Authorization': [
                        'users'
                    ]
                }
            ]
        }
    }
}

definitions = {

    ### Users ###
    'UserPostSchema': convert_to_swagger_dict(usersschemas.UserPostSchema()),
    'UserGetSchema': convert_to_swagger_dict(usersschemas.UserGetSchema()),
    'UsersGetSchema': {
        'type': 'object',
        'properties': {
            'users': {
                'type': 'array',
                'items': {
                    '$ref': '#/definitions/UserGetSchema'
                }
            }
        }
    },
    'UserLoginSchema': convert_to_swagger_dict(usersschemas.UserLoginSchema()),
    'UserLoginResponseSchema': convert_to_swagger_dict(usersschemas.UserLoginResponseSchema()),

    ### Vehicles ###
    'VehiclePostSchema': convert_to_swagger_dict(vehiclesschemas.VehiclePostSchema()),
    'VehicleGetSchema': convert_to_swagger_dict(vehiclesschemas.VehicleGetSchema()),
    'VehiclesGetSchema': {
        'type': 'object',
        'properties': {
            'vehicles': {
                'type': 'array',
                'items': {
                    '$ref': '#/definitions/VehicleGetSchema'
                }
            }
        }
    },
    'VehiclePatchSchema': convert_to_swagger_dict(vehiclesschemas.VehiclePatchSchema()),

}

doc_swagger = {
    "paths": paths,
    "definitions": definitions
}
