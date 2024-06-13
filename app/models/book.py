from django.db import models
from django.conf import settings
from .base import BaseModel
from django.db.models import Avg


class Book(BaseModel):
    """book model"""

    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    publication_date = models.DateField()
    image = models.ImageField(upload_to="book_images/", null=True, blank=True)
    published_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="books_published",
    )

    def __str__(self):
        return self.title

    @property
    def average_rating(self):
        return self.reviews.aggregate(Avg("rating"))["rating__avg"]

    class Meta:
        db_table = "books"


class Review(BaseModel):
    """review model"""

    rating_choices = [
        (1, "1 star"),
        (2, "2 stars"),
        (3, "3 stars"),
        (4, "4 stars"),
        (5, "5 stars"),
    ]
    review_message = models.TextField()
    rating = models.PositiveSmallIntegerField(default=0, choices=rating_choices)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name="reviews_written",
    )
    book_reviewed = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="reviews"
    )

    class Meta:
        """a single review for a single book"""

        unique_together = ["reviewed_by", "book_reviewed"]
        ordering = ["-created_at"]
        db_table = "reviews"
