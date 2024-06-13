from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings
from app.models import CustomUser
import logging


def get_user_from_token(token):
    """decode token and get the user"""

    try:
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        print(decoded)
        user_id = decoded.get("user_id")
        user = CustomUser.objects.get(id=user_id)
        return user
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Token has expired")
    except jwt.InvalidTokenError:
        raise AuthenticationFailed("Invalid token")
    except CustomUser.DoesNotExist:
        raise AuthenticationFailed("User does not exist")


class CustomIsAuthenticated(permissions.BasePermission):
    """keep currently logged in user in request.user"""

    def has_permission(self, request, view):
        token = request.headers.get("Authorization")
        if token is None:
            raise AuthenticationFailed("No token provided")

        try:
            token = token.split(" ")[1]
            user = get_user_from_token(token)
            request.user = user
            return True
        except AuthenticationFailed as e:
            raise e

        return False
