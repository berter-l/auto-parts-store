import logging

from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .backend import EmailBackend
from .models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer

logger = logging.getLogger('django')


class RegistrationView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    @extend_schema(
        summary="Регистрация пользователя",
        description="Создает нового пользователя и возвращает пару JWT токенов (access и refresh)."
    )
    def post(self, request):
        user_serializer = RegisterSerializer(data=request.data)
        if user_serializer.is_valid(raise_exception=True):
            try:
                with transaction.atomic():
                    user = user_serializer.save()
                    refresh = RefreshToken.for_user(user)

                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token)
                    }, status=200)

            except Exception as e:
                logger.error(f"Registration error for email {request.data.get('email')}: {str(e)}")
                print('bad')
                return Response('ошибка на стороне сервера, пожалуйста, повторите попытку позже', status=500)
        else:
            return Response(user_serializer.errors, status=400)


class UpdateJWTView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        summary="Обновление JWT токенов",
        description="Принимает refresh токен, добавляет его в черный список и выдает новую пару токенов."
    )
    def post(self, request):
        token = request.data.get('refresh')
        try:
            refresh = RefreshToken(token)
            id = refresh['user_id']
            refresh.blacklist()
            new_token = RefreshToken.for_user(CustomUser.objects.get(id=id))
            return Response({"refresh": str(new_token), "access": str(new_token.access_token)}, status=200)

        except Exception as e:
            logger.error(f"JWT update error: {str(e)}")
            return Response({'the token is not valid': str(e)}, status=400)


class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        summary="Выход из системы",
        description="Добавляет refresh токен в черный список, завершая сессию пользователя."
    )
    def post(self, request):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

        except Exception as e:
            logger.error(f"Logout error for user {request.user.email}: {str(e)}")
            return Response({'error': 'Invalid update token'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Выход завершен успешно'}, status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    @extend_schema(
        summary="Вход в систему",
        description="Аутентифицирует пользователя по email и паролю, возвращает пару JWT токенов."
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            try:
                user = EmailBackend().authenticate(request, email=request.data['email'],
                                                   password=request.data['password'])
                if user is not None:
                    refresh = RefreshToken.for_user(user)
                    return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=200)
                else:
                    return Response({'error': 'Неверный адрес электронной почты или пароль'},
                                    status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                logger.error(f"Login error for email {request.data['email']}: {str(e)}")
                return Response({'error': 'Ошибка сервера при входе'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


