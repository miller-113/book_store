from django.urls import path
from .views import book_list, add_book, books_with_matching_authors

urlpatterns = [
    path('', book_list, name='book_list'),
    path('add/', add_book, name='add_book'),
    path('matching-authors/', books_with_matching_authors, name='books_with_matching_authors'),
]