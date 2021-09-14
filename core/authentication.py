import jwt
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from rara_api import settings 
from core.utils import jwt_decode_handler

class JwtTokenAuthentication(BaseAuthentication):
    '''
        Custom authentication class for validating incoming token
        https://www.django-rest-framework.org/api-guide/authentication/#custom-authentication
    '''
    keyword = settings.MY_JWT_CONF.get('JWT_HEADER_PREFIX', 'Bearer')

    def authenticate(self, request):

        User = get_user_model()
        authorization_header = request.headers.get('Authorization')

        auth = authorization_header and authorization_header.split(' ') 

        if not authorization_header or auth[0].lower() != self.keyword.lower():
            return None
        try:
            jwt_token = auth[1]
            payload = jwt_decode_handler(jwt_token) 

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token expired')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()

        try:
            user = User.objects.get(pk=payload['user_id'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        user = self.authenticate_credentials(payload)

        return (user, None)

    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id.
        """
        User = get_user_model()

        try:
            user = User.objects.get(pk=payload['user_id'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return user

    def authenticate_header(self, request):
        return self.keyword