# from django.contrib.auth import get_user_model
from rest_framework import serializers
from app.models import Book, CustomUser

from .review_serializer import ReviewSerializer


class BookSerializer(serializers.ModelSerializer):
    average_rating = serializers.DecimalField(
        max_digits=3, decimal_places=2, read_only=True
    )
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "publication_date",
            "price",
            "published_by",
            "average_rating",
            "reviews",
        ]
        extra_kwargs = {"id": {"read_only": True}}
