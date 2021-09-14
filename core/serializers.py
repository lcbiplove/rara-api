from rest_framework import serializers
from django.contrib.auth import authenticate
from core.utils import jwt_get_payload, jwt_encode_payload


class LoginSerializer(serializers.Serializer):
    """Serializes user input and authenticate"""
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={
            'input_type': 'password'
        }
    )

    class Meta:
        fields = ('email', 'password')

    def validate(self, attrs):
        credentials = {
            'email': attrs.get('email'),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            user = authenticate(**credentials)

            if user:
                payload = jwt_get_payload(user)

                return {
                    'token': jwt_encode_payload(payload),
                }
            else:
                mssg = 'Invalid login credentials.'
                raise serializers.ValidationError(mssg)
        else:
            mssg = 'Include "email" and "password".'
            raise serializers.ValidationError(mssg)
