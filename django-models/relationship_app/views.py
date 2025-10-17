from django.shortcuts import render, redirect
from .models import Book, Library
from django.views.generic import DetailView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
# relationship_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .models import Book, Author

# views.py

from django.contrib.auth.decorators import login_required, user_passes_test
from .models import UserProfile
# Function-Based View — List all books
def list_books(request):
    books = Book.objects.select_related('author').all()
    context = {'books': books}
    return render(request, 'list_books.html', context)

# Class-Based View — Show one library and its books
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'

# Registration view
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books')
        else:
            messages.error(request, "Registration failed. Please try again.")
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('list_books')
        else:
            messages.error(request, "Login failed. Please check your username and password.")
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    return render(request, 'relationship_app/logout.html')



def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == UserProfile.ROLE_ADMIN

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == UserProfile.ROLE_LIBRARIAN

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == UserProfile.ROLE_MEMBER

@login_required
@user_passes_test(is_admin, login_url='/no-permission/')
def admin_view(request):
    # Render the admin template
    return render(request, 'relationship_app/admin_view.html', {'user': request.user})

@login_required
@user_passes_test(is_librarian, login_url='/no-permission/')
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html', {'user': request.user})

@login_required
@user_passes_test(is_member, login_url='/no-permission/')
def member_view(request):
    return render(request, 'relationship_app/member_view.html', {'user': request.user})

# Simple view to show when someone lacks permission
from django.http import HttpResponse

def no_permission(request):
    return HttpResponse("You do not have permission to view this page.", status=403)



# List all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/book_list.html', {'books': books})


# Create a book (requires can_add_book permission)
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    authors = Author.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        author = get_object_or_404(Author, id=author_id)
        Book.objects.create(title=title, author=author)
        return redirect('list_books')
    return render(request, 'relationship_app/add_book.html', {'authors': authors})


# Edit a book (requires can_change_book permission)
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    authors = Author.objects.all()
    if request.method == 'POST':
        book.title = request.POST.get('title')
        author_id = request.POST.get('author')
        book.author = get_object_or_404(Author, id=author_id)
        book.save()
        return redirect('list_books')
    return render(request, 'relationship_app/edit_book.html', {'book': book, 'authors': authors})


# Delete a book (requires can_delete_book permission)
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    return render(request, 'relationship_app/delete_book.html', {'book': book})
