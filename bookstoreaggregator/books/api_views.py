from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer
from django_filters import rest_framework as filters

class BookFilter(filters.FilterSet):
    genre = filters.CharFilter(field_name='genre', lookup_expr='icontains')
    store = filters.CharFilter(field_name='store', lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ['genre', 'store']

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter
