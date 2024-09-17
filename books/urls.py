from django.urls import path
from .views import book_list, add_book

urlpatterns = [
    path('add/', add_book, name='add_book'),
    path('', book_list, name='book_list'),
]