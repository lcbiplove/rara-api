from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class JwtTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'


class LoginView(APIView):
    authentication_classes = [JwtTokenAuthentication,]
    permission_classes = [IsAuthenticated,]

    def post(self, request, *args, **kwargs):
        return Response({})