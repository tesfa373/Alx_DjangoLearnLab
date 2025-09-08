from django.urls import path
from .views import list_books, LibraryDetailView

urlpatterns = [
    path("", list_books, name="home"),                    # root URL: list books in plain text
    path("books/", list_books, name="list_books"),       # optional extra route
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),
]
