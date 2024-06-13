from django.contrib.auth import authenticate
from app.accessors import UserAccessor
from django.contrib.auth.hashers import make_password
from app.helpers import get_tokens_for_user


class UserService:
    """user service to handle the business logic for users"""

    @staticmethod
    def user_login(email, password):
        user = authenticate(email=email, password=password)
        if user is not None:
            return get_tokens_for_user(user)
        return None

    @staticmethod
    def register_user(register_data):
        register_data["password"] = make_password(register_data["password"])
        user = UserAccessor.register(register_data)
        return user
