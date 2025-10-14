from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Book, Library
from django.views.generic import DetailView

# 📘 Function-Based View — List all books
def list_books(request):
    books = Book.objects.select_related('author').all()
    context = {'books': books}
    return render(request, 'list_books.html', context)
# 🏛️ Class-Based View — Show one library and its books
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'
