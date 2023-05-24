from cerberus import Validator

BodySchema = {
    "create_meeting_schema": {
        'topic': {'type': 'string', "maxlength": 100, 'required': True},
        'date': {'type': 'string', "maxlength": 10, 'required': True},
        'start_time': {'type': 'string', "maxlength": 5, 'required': True},
        'end_time': {'type': 'string', "maxlength": 5, 'required': True},
        'participants': {'type': 'list', 'minlength': 1, 'required': True}
    },
    "update_meeting_schema": {
        'topic': {'type': 'string', 'maxlength': 100},
        'date': {'type': 'string', 'maxlength': 10},
        'start_time': {'type': 'string', 'maxlength': 5},
        'end_time': {'type': 'string', 'maxlength': 5},
        'participants': {'type': 'list', 'minlength': 1}
    },
    "id_schema": {
        'id': {'type': 'integer', 'required': True}
    }
}

ParamsSchema = {
    "id_schema": {
        'id': {'type': 'integer', 'required': True}
    }
}


def validate_body(request, schema_name):
    print(schema_name)
    v = Validator(BodySchema[schema_name])
    request_data = request.get_json()
    if not v.validate(request_data):
        return v.errors
    return None

def validate_id(id):
    v = Validator(ParamsSchema["id_schema"])
    if not v.validate({"id": id}):
        return v.errors
    return None