from django.shortcuts import render, redirect, get_object_or_404
from django.forms import formset_factory
from django.db.models import Count, F
from django.core.exceptions import PermissionDenied

from .models import Book, Author, Tag, HttpRequestLog
from .serializers import BookSerializer
from .forms import BookForm, AuthorInlineFormset


def books_with_matching_authors(request):
    books = Book.objects.filter(authors__first_name=F('authors__last_name')).distinct()
    return render(request, 'books/books_with_matching_authors.html', {'books': books})


def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})


def add_book(request):
    if request.method == 'POST':
        book_form = BookForm(request.POST)
        formset = AuthorInlineFormset(request.POST, instance=Book())

        if book_form.is_valid() and formset.is_valid():
            book_data = book_form.cleaned_data
            book = Book.objects.create_book(
                store=book_data['store'],
                title=book_data['title'],
                genre=book_data['genre'],
                isbn=book_data['isbn'],
                price=book_data['price'],
                count=book_data['count'],
                publish_date=book_data.get('publish_date')
            )
            formset.instance = book
            formset.save()
            return redirect('/books/')
    else:
        book_form = BookForm()
        formset = AuthorInlineFormset(instance=Book())

    return render(request, 'books/add_book.html', {'book_form': book_form, 'formset': formset})


def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if book.owner != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        book_form = BookForm(request.POST, instance=book)
        formset = AuthorInlineFormset(request.POST, instance=book)

        if book_form.is_valid() and formset.is_valid():
            book_data = book_form.cleaned_data
            Book.objects.update_book(
                book_id=book.id,
                store=book_data['store'],
                title=book_data['title'],
                genre=book_data['genre'],
                isbn=book_data['isbn'],
                price=book_data['price'],
                count=book_data['count'],
                publish_date=book_data.get('publish_date')
            )
            formset.save()
            return redirect('/books/')
    else:
        book_form = BookForm(instance=book)
        formset = AuthorInlineFormset(instance=book)

    return render(request, 'books/edit_book.html', {'book_form': book_form, 'formset': formset})


def last_10_requests(request):
    last_10_logs = HttpRequestLog.objects.order_by('-timestamp')[:10]
    return render(request, 'books/last_10_requests.html', {'logs': last_10_logs})
