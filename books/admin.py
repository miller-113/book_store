from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('store', 'title', 'genre', 'isbn', 'price', 'count', 'author_list')

    def author_list(self, obj):
        return ", ".join(author.name for author in obj.authors.all())
    author_list.short_description = 'Authors'

admin.site.register(Book, BookAdmin)