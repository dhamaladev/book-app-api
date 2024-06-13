from rest_framework import permissions
from app.models import Book, Review


class IsAdminOrOwner(permissions.BasePermission):
    """only either admin or the owner are allowed to perform action using this permission class"""

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True
        if isinstance(obj, Book):
            return obj.published_by == request.user
        if isinstance(obj, Review):
            return obj.reviewed_by == request.user
        return False
