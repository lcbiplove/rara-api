from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.serializers import LoginSerializer



class JwtTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            token = serializer.validated_data.get('token')
            return Response({
                'token': token
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)