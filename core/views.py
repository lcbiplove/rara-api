from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.serializers import LoginSerializer
from core.authentication import JwtTokenAuthentication

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

class UserProfileView(APIView):
    authentication_classes = [JwtTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response({
            'user_id': request.user.id,
            'email': request.user.email,
            'name': request.user.name,
            'location': request.user.location,
        })