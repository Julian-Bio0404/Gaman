"""Users model admin."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from gaman.users.models import User, Profile


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """User model admin."""

    list_display = [
        'pk', 'first_name', 
        'last_name', 'email', 
        'username', 'phone_number', 
        'verified', 'role',
        'created', 'updated'
    ]

    search_fields = [
        'username', 'email', 
        'first_name', 'last_name',
        'verified', 'role'
    ]

    list_filter = ['verified', 'role']
    ordering = ['first_name', 'last_name']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile model admin."""

    list_display = [
        'pk', 'user', 'sport', 
        'birth_date', 'country',
        'web_site', 'social_link',
        'created', 'updated'
    ]

    search_fields = [
        'user__username', 'user__email', 
        'user__first_name', 'user__last_name'
        'sport', 'country'
    ]

    list_filter = ['sport', 'country']
    ordering = ['user__first_name', 'user__last_name']