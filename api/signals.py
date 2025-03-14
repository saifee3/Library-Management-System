from django.db.models.signals import  m2m_changed
from django.dispatch import receiver
from django.utils import timezone
from .models import Borrower, Book

@receiver(m2m_changed, sender=Borrower.books_borrowed.through)
def update_last_borrowed_date(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        added_books = Book.objects.filter(pk__in=pk_set)
        for book in added_books:
            book.last_borrowed_date = timezone.now()
            book.save()