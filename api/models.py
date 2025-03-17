from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver 
from django.utils import timezone

class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)  
     
class Book(models.Model):
    title = models.CharField(max_length=255)
    isbn = models.CharField( max_length=13, unique=True)
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    published_date = models.DateField()
    available = models.BooleanField(default=True)  
    last_borrowed_date = models.DateTimeField(null=True, blank=True)

class Borrower(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='borrower')
    books_borrowed = models.ManyToManyField(Book, blank=True, related_name='borrowers',)

@receiver(post_save, sender=User)
def manage_borrower(sender, instance, created, **kwargs):
    if created:
        Borrower.objects.create(user=instance)
    else:
        instance.borrower.save()        
