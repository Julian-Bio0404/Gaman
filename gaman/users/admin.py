"""Users model admin."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from gaman.users.models import FollowRequest, FollowUp, Profile, User


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
    ordering = ['-pk','first_name', 'last_name']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile model admin."""

    list_display = [
        'pk', 'user', 'sport', 
        'birth_date', 'country',
        'public', 'web_site',
        'social_link',
        'created', 'updated'
    ]

    search_fields = [
        'user__username', 'user__email', 
        'user__first_name', 'user__last_name'
        'sport', 'country', 'public'
    ]

    list_filter = ['sport', 'country', 'public']
    ordering = ['user__first_name', 'user__last_name']


@admin.register(FollowRequest)
class FollowRequestAdmin(admin.ModelAdmin):
    """Follow Request admin."""

    list_display = [
        'pk', 'follower', 'followed',
        'accepted', 'created'
    ]

    search_fields = [
        'follower__username', 'followed__username',
        'accepted'
    ]

    list_filter = ['accepted']


@admin.register(FollowUp)
class FollowUpAdmin(admin.ModelAdmin):
    """FollowUp model admin."""

    list_display = [
        'pk', 'follower',
        'user', 'brand',
        'club', 'created'
    ]

    search_fields = [
        'follower__username', 'user__username',
        'brand__slugname', 'club__slugname'
    ]