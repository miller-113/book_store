from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models

def validate_integer_price(value):
    if value != int(value):
        raise ValidationError('The price must be integer')

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
