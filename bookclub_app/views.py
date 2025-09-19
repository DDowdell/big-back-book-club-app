from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Book, Comment, BookSuggestion, Vote, UserBookRead
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class Home(LoginView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_book"] = Book.objects.filter(is_current=True).first()
        return context


def about(request):
    return render(request, "about.html")


@login_required
def book_index(request):
    books = Book.objects.filter(user=request.user)
    return render(request, "books/index.html", {"books": books})


@login_required
def book_detail(request, book_id):
    book = Book.objects.filter(id=book_id).first()
    if not book:
        return redirect("home")

    comments = Comment.objects.filter(book=book)
    suggestions = BookSuggestion.objects.filter(suggested_book=book)
    read_count = UserBookRead.objects.filter(book=book, has_read=True).count()

    return render(
        request,
        "books/detail.html",
        {
            "book": book,
            "comments": comments,
            "suggestions": suggestions,
            "read_count": read_count,
        },
    )


class BookCreate(LoginRequiredMixin, CreateView):
    model = Book
    fields = ["title", "author", "description", "genre", "is_current"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BookUpdate(LoginRequiredMixin, UpdateView):
    model = Book
    fields = ["author", "description", "genre", "is_current"]


class BookDelete(LoginRequiredMixin, DeleteView):
    model = Book
    success_url = "/books/"


def signup(request):
    error_message = ""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("book-index")
        else:
            error_message = "Invalid sign up - try again"
    form = UserCreationForm()
    context = {"form": form, "error_message": error_message}
    return render(request, "signup.html", context)


@login_required
def community_page(request):
    current_book = Book.objects.filter(is_current=True).first()
    comments = Comment.objects.filter(book=current_book) if current_book else []
    suggestions = BookSuggestion.objects.filter(suggested_book=current_book) if current_book else []

    return render(
        request,
        "community.html",
        {
            "current_book": current_book,
            "comments": comments,
            "suggestions": suggestions,
        },
    )

@login_required
def add_comment(request, book_id):
    if request.method == "POST":
        book = Book.objects.filter(id=book_id).first()
        if book:
            content = request.POST["content"]
            Comment.objects.create(book=book, user=request.user, content=content)
    return redirect("book-detail", book_id=book_id)


@login_required
def delete_comment(request, comment_id):
    comment = Comment.objects.filter(id=comment_id, user=request.user).first()
    if comment:
        comment.delete()
    return redirect("book-detail", book_id=comment.book.id if comment else None)


@login_required
def suggest_book(request):
    if request.method == "POST":
        suggested_book_id = request.POST["book_id"]
        BookSuggestion.objects.create(
            user=request.user, suggested_book_id=suggested_book_id
        )
        return redirect("book-detail", book_id=suggested_book_id)


@login_required
def undo_suggestion(request, suggestion_id):
    suggestion = BookSuggestion.objects.filter(
        id=suggestion_id, user=request.user
    ).first()
    if suggestion:
        suggestion.delete()
    return redirect(
        "book-detail", book_id=suggestion.suggested_book.id if suggestion else None
    )


@login_required
def vote_for_suggestion(request, suggestion_id):
    if request.method == "POST":
        suggestion = BookSuggestion.objects.filter(id=suggestion_id).first()
        if suggestion:
            Vote.objects.create(user=request.user, suggested_book=suggestion)
            return redirect("book-detail", book_id=suggestion.suggested_book.id)
