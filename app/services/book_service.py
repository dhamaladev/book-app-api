from app.accessors import BookAccessor
from django.core.exceptions import ValidationError


class BookService:
    @staticmethod
    def get_all_books(query_params, request):
        return BookAccessor.get_all_books(query_params, request)

    def get_book_by_id(book_id):
        try:
            return BookAccessor.get_book_by_id(book_id)
        except ValidationError:
            raise ValueError("Invalid UUID format for book ID")