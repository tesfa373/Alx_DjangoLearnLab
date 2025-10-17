from django.contrib import admin

# Register your models here.
# # admin.py
# from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_select_related = ('user',)
    search_fields = ('user__username', 'role')
