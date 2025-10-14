

# Register your models here.
from django.contrib import admin
from .models import Book

# Customize admin display
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Columns to show in list view
    list_filter = ('author', 'publication_year')           # Filter sidebar
    search_fields = ('title', 'author')                    # Search box fields

# Register the model with custom admin
admin.site.register(Book, BookAdmin)
