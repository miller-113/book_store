from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

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

    def assign_default_tag(self):
        if not self.tags.exists():
            default_tag, _created = Tag.objects.get_or_create(name='tag_not_set')
            self.tags.add(default_tag)

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


@receiver(post_save, sender=Book)
def handle_book_save(sender, instance, **kwargs):
    instance.assign_default_tag()

@receiver(m2m_changed, sender=Book.tags.through)
def handle_book_tags_change(sender, instance, action, **kwargs):
    if action == 'post_remove' or action == 'post_clear':
        if not instance.tags.exists():
            default_tag, _created = Tag.objects.get_or_create(name='tag_not_set')
            instance.tags.add(default_tag)
