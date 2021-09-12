from rest_framework import serializers
from core.models import UserProfile
from django.contrib.auth import authenticate
from core.utils import get_jwt_payload, encode_jwt_payload

class LoginSerializer(serializers.ModelSerializer):
    """Serializes user input and authenticate"""

    class Meta:
        model = UserProfile
        fields = ('email', 'password')

    def validate(self, attrs):
        credentials = {
            'email': attrs.get('email'),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            user = authenticate(**credentials)

            if user:
                payload = get_jwt_payload(user)

                return {
                    'token': encode_jwt_payload(payload),
                    'user': user
                }
            else:
                mssg = 'Invalid login credentials.'
                raise serializers.ValidationError(mssg)
        else:
            mssg = '"email" and "password" not included.'
            raise serializers.ValidationError(mssg)

    