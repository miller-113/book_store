from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import BookViewSet, BookCreateApiView

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('books/create/', BookCreateApiView.as_view(), name='book-create'),
]