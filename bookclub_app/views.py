from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Book
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class Home(LoginView):
    template_name = "home.html"


def about(request):
    return render(request, "about.html")


@login_required
def book_index(request):
    books = Book.objects.filter(user=request.user)
    return render(request, "books/index.html", {"books": books})


@login_required
def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    return render(request, "books/detail.html", {"book": book})


class BookCreate(LoginRequiredMixin, CreateView):
    model = Book
    fields = "__all__"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BookUpdate(LoginRequiredMixin, UpdateView):
    model = Book
    fields = ["author", "description", "genre"]


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
