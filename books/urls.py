from django.urls import path
from .views import book_list, add_book, books_with_matching_authors, edit_book, last_10_requests

urlpatterns = [
    path('', book_list, name='book_list'),
    path('<int:book_id>/edit/', edit_book, name='edit_book'),
    path('add/', add_book, name='add_book'),
    path('matching-authors/', books_with_matching_authors, name='books_with_matching_authors'),
    path('last-10-requests/', last_10_requests, name='last_10_requests'),
]