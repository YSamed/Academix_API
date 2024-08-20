from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import TokenSerializer
from rest_framework_simplejwt.views import TokenRefreshView

class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        serializer = TokenSerializer({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })

        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutAPIView(APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception as e:
                return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'detail': 'Successfully logged out'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'No refresh token provided'}, status=status.HTTP_400_BAD_REQUEST)



class CustomTokenRefreshView(TokenRefreshView):
    pass