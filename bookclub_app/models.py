from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    genre = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book-detail", kwargs={"book_id": self.id})


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class UserBookRead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    has_read = models.BooleanField(default=False)


class Comment(models.Model):
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"Comment by {self.user.username} on {self.book.title}"


class BookSuggestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    suggested_book = models.ForeignKey("Book", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Suggestion by {self.user.username} for {self.suggested_book.title}"


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    suggested_book = models.ForeignKey(BookSuggestion, on_delete=models.CASCADE)

    def __str__(self):
        return f"Vote by {self.user.username} for {self.suggested_book.suggested_book.title}"
