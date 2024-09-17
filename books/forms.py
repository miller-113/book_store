from django import forms
from django.forms import inlineformset_factory
from .models import Book, Author

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['store', 'title', 'genre', 'isbn', 'price', 'count']
        
    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        if not isbn.startswith('9'):
            raise forms.ValidationError("ISBN must start with '9'.")
        return isbn

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name']


AuthorInlineFormset = inlineformset_factory(
    Book, Author, form=AuthorForm, extra=2
)
