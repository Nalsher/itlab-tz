from rest_framework import serializers

from user.models import User


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=False,
    )
    username = serializers.CharField(max_length=128)
    password = serializers.CharField(max_length=32)

    class Meta:
        model = User
        fields = ["email", "username", "password"]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class TokenRegistrySerializer(serializers.Serializer):
    token = serializers.CharField()
    chat_id = serializers.CharField()
