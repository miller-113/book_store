from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver


def validate_integer_price(value):
    if isinstance(value, float):
        value = Decimal(value)
    elif not isinstance(value, Decimal):
        raise ValidationError('Invalid type for price')

    if value != value.to_integral_value():
        raise ValidationError('The price must be an integer')

class BookManager(models.Manager):
    def create_book(self, **kwargs):
        book = self.model(**kwargs)
        book.full_clean() 
        if not book.tags.exists():
            default_tag, _created = Tag.objects.get_or_create(name='tag_not_set')
            book.tags.add(default_tag)
        book.save()
        return book
    
    def update_book(self, book_id, **kwargs):
        book = self.get(pk=book_id)
        for attr, value in kwargs.items():
            setattr(book, attr, value)
        book.full_clean()
        if not book.tags.exists():
            default_tag, _created = Tag.objects.get_or_create(name='tag_not_set')
            book.tags.add(default_tag)
        book.save()
        return book

class Book(models.Model):
    store = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MaxValueValidator(100),
            validate_integer_price 
        ]
    )
    count = models.IntegerField()
    tags = models.ManyToManyField('Tag', related_name='books', blank=True)
    publish_date = models.DateField(null=True, blank=True) 
    
    objects = BookManager()

    @property
    def tag_count(self):
        return self.tags.count()

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    book = models.ForeignKey(Book, related_name='authors', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class HttpRequestLog(models.Model):
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=100, blank=True, null=True)
    remote_addr = models.CharField(max_length=45)

    def __str__(self):
        return f"{self.method} {self.path} at {self.timestamp}"
