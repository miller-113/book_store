from rest_framework import serializers
from .models import Book
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
    tag_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Book
        fields = [
            'id',
            'store',
            'title',
            'genre',
            'isbn',
            'price',
            'count',
            'tags',
            'publish_date',
            "tag_count",
        ]

    def validate_isbn(self, value):
        if not value.startswith('9'):
            raise serializers.ValidationError("ISBN must start with '9'.")
        return value

    def validate(self, data):
        current_hour = datetime.now().hour
        if 1 <= current_hour < 5:
            raise serializers.ValidationError("Form cannot be submitted between 1 am and 5 am.")
        return data
