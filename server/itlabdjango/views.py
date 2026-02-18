import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import IntegrityError
from rest_framework_simplejwt.tokens import RefreshToken

from itlabdjango.serializers import RegisterSerializer, LoginSerializer
from user.models import User

from itlabdjango.serializers import TokenRegistrySerializer

logger = logging.getLogger(__name__)


class RegsiterApiView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                serializer.save()
                return Response(data=serializer.data, status=201)
            except IntegrityError as error_code:
                logger.error(error_code)
                return Response(data={"error": "Already exist"}, status=400)
        return Response(serializer.errors, status=400)


class LoginApiView(APIView):
    serializer_class = LoginSerializer

    def check_permissions(self, request):
        return True

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password").strip()

        if not email or not password:
            return Response(
                {"error": "Email and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user: User = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.check_password(password) and user.password != password:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
        try:
            refresh: RefreshToken = RefreshToken.for_user(user)

            data = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "telegram_token": user.telegram_token,
                "profile": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "name": user.first_name + " " + user.last_name,
                },
            }
            return Response(
                data,
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": "An error occurred while generating tokens", "e": repr(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class TelegramRegistryView(APIView):
    serializer_class = TokenRegistrySerializer

    def post(self, request):
        token = request.data.get("token")
        chat_id = request.data.get("chat_id")

        user = User.objects.filter(telegram_token=token).first()
        if not user:
            return Response(
                {"error": "invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        user.chat_id = chat_id
        user.save()
        return Response(
            {"success": "token has been registred"}, status=status.HTTP_200_OK
        )
