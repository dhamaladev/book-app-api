from rest_framework.response import Response
from rest_framework import status
from app.models import Book
from app.serializers import BookSerializer
from app.utils import CustomIsAuthenticated
from rest_framework.permissions import AllowAny
from app.services import BookService
from app.builders import ResponseBuilder
from rest_framework.decorators import api_view, permission_classes
from app.helpers import IsAdminOrOwner
from app.builders import api


@api_view(["GET"])
@permission_classes([AllowAny])
def book_list_view(request):
    """List all the books"""

    query_params = request.query_params
    response_builder = ResponseBuilder()
    books, page_info = BookService.get_all_books(query_params, request)
    serializer = BookSerializer(books, many=True)
    response_data = {
        'results': serializer.data,
        'page_info': page_info,
    }
    return response_builder.get_200_success_response(
        "Books retrieved successfully", response_data
    )


@api_view(["POST"])
@permission_classes([CustomIsAuthenticated, IsAdminOrOwner])
def book_create_view(request):
    """
    Create a book.
    """
    data = request.data.copy()
    data["published_by"] = request.user.id
    response_builder = ResponseBuilder()
    serializer = BookSerializer(data=data)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(
            api.INVALID_INPUT, serializer.errors
        )
    serializer.save()
    return response_builder.get_201_success_response(
        "book created successfully", serializer.data
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def book_detail_view(request, pk):
    """get a book by id"""

    response_builder = ResponseBuilder()
    book = BookService.get_book_by_id(pk)
    if not book:
        return response_builder.get_404_not_found_response(api.BOOK_NOT_FOUND)
    serializer = BookSerializer(book)
    return response_builder.get_200_success_response(
        "book retrieved successfully", serializer.data
    )


@api_view(["PUT"])
@permission_classes([CustomIsAuthenticated, IsAdminOrOwner])
def book_update_view(request, pk):
    """update a book"""

    response_builder = ResponseBuilder()
    book = BookService.get_book_by_id(pk)
    if not book:
        return response_builder.get_404_not_found_response(api.BOOK_NOT_FOUND)
    if book.published_by != request.user:
        return response_builder.get_400_bad_request_response(
            api.UNAUTHORIZED, "user not authorized"
        )
    serializer = BookSerializer(book, data=request.data, partial=True)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(
            api.INVALID_INPUT, serializer.errors
        )
    serializer.save()
    return response_builder.get_201_success_response(
        "book updated successfully", serializer.data
    )


@api_view(["DELETE"])
@permission_classes([CustomIsAuthenticated, IsAdminOrOwner])
def book_delete_view(request, pk):
    """delete a book"""

    response_builder = ResponseBuilder()
    book = BookService.get_book_by_id(pk)
    if book is None:
        return response_builder.get_404_not_found_response(api.BOOK_NOT_FOUND)
    if book.published_by != request.user:
        return response_builder.get_400_bad_request_response(
            api.UNAUTHORIZED, "user not authorized"
        )

    book.is_deleted = True
    book.save()
    return response_builder.get_204_success_response()
