from rest_framework import serializers
from .models import Book
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def validate_isbn(self, value):
        if not value.startswith('9'):
            raise serializers.ValidationError("ISBN must start with '9'.")
        return value

    def validate(self, data):
        current_hour = datetime.now().hour
        if 1 <= current_hour < 5:
            raise serializers.ValidationError("Form cannot be submitted between 1 am and 5 am.")
        return data
