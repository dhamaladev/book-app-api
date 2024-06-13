from app.models import Book
from django.core.exceptions import ValidationError
from django.db.models import Q
from app.helpers import paginate


class BookAccessor:
    """book accessor to handle the database logic"""

    @staticmethod
    def get_all_books(query_params, request):
        """Filter and search books based on query parameters"""

        queryset = Book.objects.filter(is_deleted=False)
        filter_criteria = Q()

        for param, value in query_params.items():
            if hasattr(Book, param):
                filter_criteria &= Q(**{f"{param}__icontains": value})
        if filter_criteria:
            queryset = queryset.filter(filter_criteria)

        paginated_queryset, page_info = paginate(queryset, request)
        return paginated_queryset, page_info

    @staticmethod
    def get_book_by_id(book_id):
        """get book by id"""

        try:
            return Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return None
        except ValidationError:
            raise ValueError("Invalid UUID format for book ID")
