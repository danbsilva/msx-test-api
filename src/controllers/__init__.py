from marshmallow import ValidationError

def validate_schema(schema, payload):
    try:
        schema.load(payload)
    except ValidationError as e:
        return e.messages