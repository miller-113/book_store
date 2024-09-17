from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models

def validate_integer_price(value):
    if value != int(value):
        raise ValidationError('The price must be integer')


class Author(models.Model):
    name = models.CharField(max_length=100)
    book = models.ForeignKey('Book', related_name='authors', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
        
        
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

    def __str__(self):
        return self.title
