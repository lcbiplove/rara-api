import datetime
from rara_api import settings

def get_jwt_payload(user) -> dict:
    """ Returns payload of dictionary from user object """
    payload = {
        'user_id': user.pk,
        'email': user.email,
        'name': user.name,
        'location': user.location,
        'exp': datetime.utcnow() + settings.MY_JWT_CONF['JWT_EXPIRATION_TIME'],
        'exp': datetime.utcnow(),
    }
    return payload

def encode_jwt_payload(payload):
    return {}