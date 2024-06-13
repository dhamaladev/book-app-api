from django.contrib import admin
from app.models import CustomUser, Book, Review


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name", "is_admin", "email"]


class BookAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "price", "publication_date"]


class ReviewAdmin(admin.ModelAdmin):
    list_display = ["id", "review_message", "rating"]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Review, ReviewAdmin)
