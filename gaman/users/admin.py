"""Users model admin."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from gaman.users.models import FollowRequest, FollowUp, Profile, User


class ProfileInline(admin.StackedInline):
    """Profile in-line admin for users."""

    model = Profile
    can_delete = False
    verbose_name_plural = 'profiles'


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """User model admin."""

    inlines = [ProfileInline]
    list_display = [
        'pk', 'profile',
        'first_name', 'last_name',
        'username', 'email',
        'phone_number', 'role',
        'verified', 'created', 'updated'
    ]

    list_display_links = ['pk', 'profile']
    list_editable = ['verified']

    readonly_fields = [
        'pk', 'profile',
        'first_name', 'last_name',
        'username', 'email',
        'phone_number', 'role',
        'created', 'updated'
    ]

    search_fields = [
        'username', 'email',
        'first_name', 'last_name',
        'verified', 'role'
    ]

    list_filter = ['verified', 'role', 'profile__country']
    ordering = ['-pk', 'first_name', 'last_name']

    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False



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

    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False


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

    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False
