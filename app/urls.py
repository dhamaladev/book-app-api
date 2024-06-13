from django.urls import path
from app.views import login_view, register_view
from rest_framework_simplejwt.views import TokenRefreshView
from app.views import (
    book_delete_view,
    book_list_view,
    book_create_view,
    book_update_view,
    book_detail_view,
    review_create_view,
    review_detail_view,
    review_update_view,
    review_list_view,
    review_delete_view,
)

urlpatterns = [
    # auth
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # books
    path("book/", book_list_view, name="list-books"),
    path("book/create/", book_create_view, name="list-create-books"),
    path("book/<str:pk>/", book_detail_view, name="get-book"),
    path("book/<str:pk>/update/", book_update_view, name="update-book"),
    path("book/<str:pk>/delete/", book_delete_view, name="delete-book"),
    # reviews
    path("review/", review_list_view, name="list-reviews"),
    path("review/create/", review_create_view, name="list-create-reviews"),
    path("review/<str:book_id>/", review_detail_view, name="get-review-for-a-book"),
    path("review/<str:pk>/update/", review_update_view, name="update-review"),
    path("review/<str:pk>/delete/", review_delete_view, name="delete-review"),
]
