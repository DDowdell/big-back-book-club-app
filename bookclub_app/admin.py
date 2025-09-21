from django.contrib import admin
from .models import Book, UserProfile, Comment, BookSuggestion, Vote, UserBookRead

admin.site.register(Book)
admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(BookSuggestion)
admin.site.register(Vote)
admin.site.register(UserBookRead)