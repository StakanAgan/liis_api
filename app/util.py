from app.api.errors import bad_request
from flask import jsonify, url_for
from app import db
from app.models import *

def check_body_response(*args, data):
    for key, value in data.items():
        if value is "" and key in args:
            return False

def check_for_difference(value, data):
    pass


def make_response(object, data):
    db.session.add(object)
    db.session.commit()
    response = jsonify(object.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for(f'api.get_{object.__name__}', id=object.id)
    return response
