import datetime
import jwt
from rara_api import settings

def jwt_get_payload(user) -> dict:
    """ Returns payload of dictionary from user object """
    
    payload = {
        'user_id': user.pk,
        'email': user.email,
        'name': user.name,
        'location': user.location,
        'exp': datetime.datetime.utcnow() + settings.MY_JWT_CONF['JWT_EXPIRATION_TIME_DELTA'],
        'exp': datetime.datetime.utcnow(),
    }
    return payload

def jwt_encode_payload(payload):
    """Encodes payload with either symmetric or asymmetrically
    signed keys """
    secret_key = settings.MY_JWT_CONF.get('JWT_PRIVATE_KEY') or settings.SECRET_KEY
    return jwt.encode(
        payload,
        secret_key,
        settings.MY_JWT_CONF['JWT_ALGORITHM']
    )