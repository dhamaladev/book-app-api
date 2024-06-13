from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from app.helpers import IsAdminOrOwner
from app.utils import CustomIsAuthenticated
from app.accessors import ReviewAccessor
from app.services import ReviewService
from app.serializers import BookSerializer, ReviewSerializer
from app.builders import ResponseBuilder
from app.builders import api


@api_view(["GET"])
@permission_classes([AllowAny])
def review_list_view(request):
    response_builder = ResponseBuilder()
    reviews = ReviewAccessor.get_all_reviews()
    serializer = ReviewSerializer(reviews, many=True)
    return response_builder.get_200_success_response(
        "Books retrieved successfully", serializer.data
    )


@api_view(["POST"])
@permission_classes([CustomIsAuthenticated, IsAdminOrOwner])
def review_create_view(request):
    response_builder = ResponseBuilder()
    book_id = request.data.get("book_reviewed")
    if book_id:
        valid_book = ReviewService.validate_book(book_id)
        if valid_book[1] != status.HTTP_200_OK:
            return response_builder.get_400_bad_request_response(
                api.INVALID_UUID, valid_book[0]
            )

        can_review = ReviewService.user_can_review_book(request.user, book_id)
        if can_review[1] != status.HTTP_200_OK:
            return response_builder.get_400_bad_request_response(
                api.BOOK_ALREAY_REVIEWD_BY_A_SPECIFIC_USER, can_review[0]
            )

    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(reviewed_by=request.user)
        return response_builder.get_201_success_response(
            "Review created successfully", serializer.data
        )
    return response_builder.get_400_bad_request_response(
        api.INVALID_INPUT, serializer.errors
    )


@api_view(["GET"])
def review_detail_view(request, book_id):
    response_builder = ResponseBuilder()
    valid_book = ReviewService.validate_book(book_id)
    if valid_book[1] != status.HTTP_200_OK:
        return response_builder.get_404_not_found_response(api.BOOK_NOT_FOUND)

    book = valid_book[0]
    book_serializer = BookSerializer(book)
    reviews = ReviewAccessor.get_reviews_by_book_id(book_id)

    if not reviews.exists():
        return response_builder.get_404_not_found_response(api.BOOK_NOT_FOUND)

    review_serializer = ReviewSerializer(reviews, many=True)
    response_data = {"book": book_serializer.data, "reviews": review_serializer.data}
    return response_builder.get_200_success_response(
        "Book and reviews retrieved successfully", response_data
    )


@api_view(["PUT"])
@permission_classes([CustomIsAuthenticated, IsAdminOrOwner])
def review_update_view(request, pk):
    response_builder = ResponseBuilder()
    valid_review = ReviewService.validate_review_access(request.user, pk)
    if valid_review[1] != status.HTTP_200_OK:
        return response_builder.get_404_not_found_response(api.USER_NOT_FOUND)

    review = valid_review[0]
    serializer = ReviewSerializer(review, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return response_builder.get_200_success_response(
            "Review updated successfully", serializer.data
        )
    return response_builder.get_400_bad_request_response(
        api.INVALID_INPUT, serializer.errors
    )


@api_view(["DELETE"])
@permission_classes([CustomIsAuthenticated, IsAdminOrOwner])
def review_delete_view(request, pk):
    response_builder = ResponseBuilder()
    valid_review = ReviewService.validate_review_access(request.user, pk)
    if valid_review[1] != status.HTTP_200_OK:
        return response_builder.get_404_not_found_response(api.USER_NOT_FOUND)

    review = valid_review[0]
    review.is_deleted = True
    review.save()
    return response_builder.get_200_success_response("Review deleted successfully", {})
