from django.shortcuts import render, redirect
from django.forms import formset_factory

from .models import Book, Author
from .forms import BookForm, AuthorInlineFormset


def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})


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
    