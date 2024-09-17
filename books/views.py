from django.shortcuts import render, redirect
from django.forms import formset_factory
from django.db.models import Count, F

from .models import Book, Author, Tag
from .forms import BookForm, AuthorInlineFormset

def books_with_matching_authors(request):
    books = Book.objects.filter(authors__first_name=F('authors__last_name')).distinct()

    return render(request, 'books/books_with_matching_authors.html', {'books': books})

def book_list(request):
    books = Book.objects.annotate(tag_count=Count('tags'))
    total_tags_count = Tag.objects.annotate(book_count=Count('books')).aggregate(total_tags=Count('id'))['total_tags']

    return render(request, 'books/book_list.html', {'books': books, 'total_tags_count': total_tags_count})

def add_book(request):
    if request.method == 'POST':
        book_form = BookForm(request.POST)
        formset = AuthorInlineFormset(request.POST, instance=Book())

        if book_form.is_valid() and formset.is_valid():
            book = book_form.save()
            formset.instance = book
            formset.save()
            return redirect('/books/')
    else:
        book_form = BookForm()
        formset = AuthorInlineFormset(instance=Book())

    return render(request, 'books/add_book.html', {'book_form': book_form, 'formset': formset})
