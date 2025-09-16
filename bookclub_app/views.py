from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse('<h1>Hello BookClub</h1>')


def about(request):
    return render(request, 'about.html')


class Book:
    def __init__(self, title, author, description, genre):
        self.title = title
        self.author = author
        self.description = description
        self.genre = genre


books = [
    Book(
      'Harry Potter Series', 
      'J.K. Rowling', 
      'The boy who lived', 
      'Fantasy',
    ),
    Book(
      'The Dark Tower Series', 
      'Stephen King', 
      'A gunslingers quest', 
      'Horror',
    ),
    Book(
        'The Duke and I: Bridgerton Series',
        'Julia Quinn',
        'Daphne loves Simon?',
        'Romance',
    ),
    Book(
        'The Wheel of Time Series',
        'Robert Jordan',
        'Save the world from the Dark One',
        'Sci-Fi',
    ),
    Book(
        'Morder is Forever Series',
        'James Patterson',
        'Murder and Investigation',
        'True Crime',
    ),
]


def book_index(request):
    return render(request, 'books/index.html', {'books': books})
