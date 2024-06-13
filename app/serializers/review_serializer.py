from rest_framework import serializers
from app.models import Review, CustomUser, Book


class ReviewSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    review_message = serializers.CharField()
    rating = serializers.ChoiceField(
        choices=[
            (1, "1 star"),
            (2, "2 stars"),
            (3, "3 stars"),
            (4, "4 stars"),
            (5, "5 stars"),
        ]
    )
    reviewed_by = serializers.PrimaryKeyRelatedField(read_only=True)
    book_reviewed = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Review.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.review_message = validated_data.get(
            "review_message", instance.review_message
        )
        instance.rating = validated_data.get("rating", instance.rating)
        instance.reviewed_by = validated_data.get("reviewed_by", instance.reviewed_by)
        instance.book_reviewed = validated_data.get(
            "book_reviewed", instance.book_reviewed
        )
        instance.save()
        return instance

    def to_representation(self, instance):
        """remove the selected fields from the response"""
        representation = super().to_representation(instance)
        representation.pop("created_at", None)
        representation.pop("updated_at", None)
        representation.pop("reviewed_by", None)
        return representation
