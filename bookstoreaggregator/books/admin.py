from django.contrib import admin
from .models import Book, Author, Tag

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'store', 'genre', 'isbn', 'price', 'count')
    search_fields = ('title', 'isbn', 'store')
    list_filter = ('genre',)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'book')
    search_fields = ('first_name', 'last_name')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
