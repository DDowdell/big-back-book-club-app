from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Book, Comment, BookSuggestion, Vote
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404


class Home(LoginView):
    template_name = 'home.html'


def about(request):
    return render(request, 'about.html')


@login_required
def book_index(request):
    books = Book.objects.filter(user=request.user)
    return render(request, 'books/index.html', {'books': books})


@login_required
def book_detail(request, book_id):
    book = Book.objects.filter(id=book_id).first()
    if book is None:
      raise Http404('Book not found')
    comments = Comment.objects.filter(book=book)
    suggestions = BookSuggestion.objects.filter(suggested_book=book)
    return render(request, 'books/detail.html', {'book': book, 'comments': comments, 'suggestions': suggestions})


class BookCreate(LoginRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'description', 'genre', 'is_current']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BookUpdate(LoginRequiredMixin, UpdateView):
    model = Book
    fields = ['author', 'description', 'genre', 'is_current']


class BookDelete(LoginRequiredMixin, DeleteView):
    model = Book
    success_url = '/books/'


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book-index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)


@login_required
def add_comment(request, book_id):
    if request.method == "POST":
        book = Book.objects.filter(id=book_id).first()
        if book is None:
            raise Http404("Book not found")
        
        content = request.POST['content']
        Comment.objects.create(book=book, user=request.user, content=content)
    return redirect('book-detail', book_id=book_id)

@login_required
def suggest_book(request):
    if request.method == "POST":
        suggested_book_id = request.POST['book_id']  # This should come from your form
        BookSuggestion.objects.create(user=request.user, suggested_book_id=suggested_book_id)
        return redirect('book-detail', book_id=suggested_book_id)

@login_required
def vote_for_suggestion(request, suggestion_id):
    if request.method == "POST":
        suggestion = BookSuggestion.objects.filter(id=suggestion_id).first()
        if suggestion is None:
            raise Http404("Suggestion not found")

        Vote.objects.create(user=request.user, suggested_book=suggestion)
        return redirect('book-detail', book_id=suggestion.suggested_book.id)