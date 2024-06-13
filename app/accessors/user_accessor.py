from app.models import CustomUser
from app.builders import ResponseBuilder
from app.builders import api


class UserAccessor:
    """user accessor to handle the database related logic for users"""

    @staticmethod
    def login(email):
        return CustomUser.objects.get(email=email)

    @staticmethod
    def register(register_data):
        return CustomUser.objects.create(**register_data)
