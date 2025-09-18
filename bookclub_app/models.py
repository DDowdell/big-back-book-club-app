from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    genre = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
      
    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'book_id': self.id})
    
