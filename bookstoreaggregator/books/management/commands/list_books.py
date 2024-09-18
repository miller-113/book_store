from django.core.management.base import BaseCommand, CommandError
from books.models import Book

class Command(BaseCommand):
    help = 'Display a list of books with the possibility to order by publish date field (asc/desc)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--order',
            choices=['asc', 'desc'],
            default='asc',
            help='Order by publish date: asc or desc'
        )

    def handle(self, *args, **options):
        order = options['order']
        if order == 'asc':
            books = Book.objects.all().order_by('publish_date')
        else:
            books = Book.objects.all().order_by('-publish_date')

        for book in books:
            self.stdout.write(f"{book.title} - {book.publish_date}")
            
            
# python manage.py list_books
# python manage.py list_books --order desc