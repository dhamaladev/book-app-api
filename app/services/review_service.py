import uuid
from rest_framework import status
from app.accessors import ReviewAccessor


class ReviewService:
    @staticmethod
    def check_uuid(book_id):
        try:
            uuid_obj = uuid.UUID(book_id)
        except ValueError:
            return False
        return True

    @staticmethod
    def validate_book(book_id):
        if not ReviewService.check_uuid(book_id):
            return {"message": "Invalid UUID format."}, status.HTTP_400_BAD_REQUEST
        book = ReviewAccessor.get_book_by_id(book_id)
        if not book:
            return {"message": "Book not found."}, status.HTTP_404_NOT_FOUND
        return book, status.HTTP_200_OK

    @staticmethod
    def user_can_review_book(user, book_id):
        if ReviewAccessor.review_exists_by_user_and_book(user, book_id):
            return {
                "message": "You have already reviewed this book."
            }, status.HTTP_400_BAD_REQUEST
        return {"success": True}, status.HTTP_200_OK

    @staticmethod
    def validate_review_access(user, review_id):
        review = ReviewAccessor.get_review_by_id(review_id)
        if not review:
            return {"message": "Review not found."}, status.HTTP_404_NOT_FOUND
        if review.reviewed_by != user:
            return {
                "message": "Not authorized to update/delete this review."
            }, status.HTTP_403_FORBIDDEN
        return review, status.HTTP_200_OK
