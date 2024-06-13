from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from app.serializers import LoginSerializer, RegisterSerializer
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from app.services import UserService
from app.builders import ResponseBuilder, api


@swagger_auto_schema(method="post", request_body=LoginSerializer, responses={200: "OK"})
@api_view(["POST"])
def login_view(request):
    """login user view"""

    response_builder = ResponseBuilder()
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        tokens = UserService.user_login(email, password)
        if tokens:
            return response_builder.get_200_success_response(
                "user logged in successfully", tokens
            )
        return response_builder.get_404_not_found_response(
            api.EMAIL_OR_PASSWORD_NOT_CORRECT
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="post",
    request_body=RegisterSerializer,
    responses={201: "Created"},
)
@api_view(["POST"])
def register_view(request):
    """register user view"""

    response_builder = ResponseBuilder()
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        new_user = UserService.register_user(serializer.validated_data)
        new_user_serialized = RegisterSerializer(new_user).data
        return response_builder.get_201_success_response(
            "User created successfully", new_user_serialized
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

