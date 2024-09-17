from datetime import datetime

from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'price', 'count')

    def save_model(self, request, obj, form, change):
        if not obj.isbn.startswith('9'):
            raise ValidationError("ISBN should start from '9'.")
        current_hour = datetime.now().hour
        if 1 <= current_hour <= 5:
            raise ValidationError("Forms cannot be submitted between 1am and 5am.")
        super().save_model(request, obj, form, change)
