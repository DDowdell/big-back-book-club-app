from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('books/', views.book_index, name='book-index'),
    path('books/<int:book_id>/', views.book_detail, name='book-detail'),
    path('books/create', views.BookCreate.as_view(), name='book-create'),
    path('books/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
    path('accounts/signup/', views.signup, name='signup'),
    path('books/<int:book_id>/add_comment/', views.add_comment, name='add_comment'),
    path('books/suggest/', views.suggest_book, name='suggest_book'),
    path('book_suggestion/<int:suggestion_id>/vote/', views.vote_for_suggestion, name='vote_for_suggestion'),
]
