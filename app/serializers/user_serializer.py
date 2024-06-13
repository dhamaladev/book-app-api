from rest_framework import serializers
from app.models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    """serializer for registering an user"""

    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email", "password")


class LoginSerializer(serializers.Serializer):
    """serializer for logging in an user"""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
