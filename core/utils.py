import datetime
import urllib
import jwt
import json
from jwt.algorithms import RSAAlgorithm
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from jwt import PyJWKClient
from django.contrib.auth import get_user_model
from rara_api import settings


DEFAULT_KID = '230498151c214b788dd97f22b85410a5'


def jwt_get_payload(user: get_user_model, exp: datetime = None) -> dict:
    """Returns payload of dictionary from user object
    Args:
        user: User object 
        exp: Expiry datetime
    """
    exp = exp or datetime.datetime.utcnow() + settings.MY_JWT_CONF['JWT_EXPIRATION_TIME_DELTA']
    
    payload = {
        'user_id': user.pk,
        'email': user.email,
        'name': user.name,
        'location': user.location,
        'exp': exp,
        'iat': datetime.datetime.utcnow(),
    }
    return payload

def jwt_encode_payload(payload: dict) -> str:
    """Encodes payload with either symmetric or asymmetrically
    signed keys 
    Args:
        payload: to be encoded data (dict)
    """

    secret_key =  settings.SECRET_KEY
    private_key_path = settings.MY_JWT_CONF.get('JWT_PRIVATE_KEY_PATH')
    if private_key_path :
        secret_key = open(private_key_path).read()

    return jwt.encode(
        payload,
        secret_key,
        settings.MY_JWT_CONF['JWT_ALGORITHM'],
        headers={'kid': DEFAULT_KID},
    )

def jwt_decode_handler(jwt_token: str) -> dict:
    """Decides either server act as monolith or as resource server
    Args:
        jwt_token: token to be decoded (str)
    """
    
    if settings.MY_JWT_CONF['JWT_DECODE_MONOLITH']:
        return jwt_decode_token_monolith(jwt_token)
    return jwt_decode_token(jwt_token)


def jwt_decode_token_monolith(jwt_token: str) -> dict:
    """Decodes incoming token and returns payload
    Args:
        jwt_token: token to be decoded (str)
    """

    public_key = open(settings.MY_JWT_CONF.get('JWT_PUBLIC_KEY_PATH')).read()

    return jwt.decode(
        jwt=jwt_token,
        key=public_key,
        algorithms=[settings.MY_JWT_CONF['JWT_ALGORITHM']]
    )

# def jwt_decode_token(jwt_token: str) -> dict:
#     url = "http://localhost:8000/api/certs/"

#     with urllib.request.urlopen(url) as response:
#         jwks = json.load(response)

#     public_keys = {}
#     for jwk in jwks['keys']:
#         kid = jwk['kid']
#         public_keys[kid] = RSAAlgorithm.from_jwk(json.dumps(jwk))

#     kid = jwt.get_unverified_header(jwt_token)['kid']
#     key = public_keys[kid]

#     return jwt.decode(
#         jwt=jwt_token,
#         key=key,
#         algorithms=[settings.MY_JWT_CONF['JWT_ALGORITHM']]
#     )

def jwt_decode_token(jwt_token: str) -> dict:
    """Decode jwt from jwks endpoint
    Args:
        jwt_token: Token
    
    https://pyjwt.readthedocs.io/en/latest/usage.html#retrieve-rsa-signing-keys-from-a-jwks-endpoint
    """

    url = settings.MY_JWT_CONF['JWT_JWKS_ENDPOINT']
    jwks_client = PyJWKClient(url, cache_keys=True)
    signing_key = jwks_client.get_signing_key_from_jwt(jwt_token)
    data = jwt.decode(
        jwt_token,
        signing_key.key,
        algorithms=[settings.MY_JWT_CONF['JWT_ALGORITHM']],
    )
    return data


def jwt_create_jwk() -> dict:
    """Create JWKS of the public rsa key"""

    public_key_path = settings.MY_JWT_CONF.get('JWT_PUBLIC_KEY_PATH')
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    loaded_json = json.loads(RSAAlgorithm.to_jwk(public_key))
    loaded_json['kid'] = DEFAULT_KID

    # use added to work with PyJWKClient
    loaded_json['use'] = 'sig'
    return loaded_json