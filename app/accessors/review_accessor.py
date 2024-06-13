from app.models import Book, Review
from django.core.exceptions import ObjectDoesNotExist

class ReviewAccessor:
    @staticmethod
    def get_all_reviews():
        return Review.objects.all()

    @staticmethod
    def get_book_by_id(book_id):
        try:
            return Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return None

    @staticmethod
    def get_reviews_by_book_id(book_id):
        return Review.objects.filter(book_reviewed_id=book_id)

    @staticmethod
    def get_review_by_id(review_id):
        try:
            return Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            return None

    @staticmethod
    def review_exists_by_user_and_book(user, book_id):
        return Review.objects.filter(reviewed_by=user, book_reviewed_id=book_id).exists()
