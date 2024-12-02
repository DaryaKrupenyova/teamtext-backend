import logging.config

from decouple import config
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterUserSerializer, LoginUserSerializer


User = get_user_model()
logger = logging.getLogger(__name__)


class RegistrationAPIView(APIView):
    """
    Эндпоинт регистрации пользователя.
    """
    def post(self, request):
        """
        Метод регистрации пользователя.
        """
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            self.user = serializer.save()
            refresh = RefreshToken.for_user(self.user)
            refresh.payload.update({
                'user_id': self.user.id,
                'email': self.user.email
            })
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    """
    Эндпоинт авторизации пользователя.
    """
    def post(self, request):
        """
        Метод авторизации пользователя.
        """
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            refresh = RefreshToken.for_user(user)
            refresh.payload.update({
                'user_id': user.id,
                'email': user.email
            })
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPIView(APIView):
    """
    Эндпоинт выхода из аккаунта пользователя.
    """
    def post(self, request):
        """
        Метод выхода из аккаунта пользователя. Если предоставлен корректный refresh токен, то
        токен попадает в blacklist.
        """
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'Необходим Refresh token'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError as err:
            return Response({'error': 'Неверный Refresh token'},
                            status=status.HTTP_403_FORBIDDEN)
        except Exception as err:
            logger.error(f"Logout failed: {err}", exc_info=True)
            return Response({'error': 'Что-то пошло не так'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': 'Выход успешен'}, status=status.HTTP_200_OK)
