"""Posts models admin."""

# Django
from django.contrib import admin

# Models
from gaman.posts.models import Comment, CommentReaction, Post, PostReaction


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Post model admin."""

    list_display = [
        'pk', 'user',
        'brand', 'club',
        'about', 'privacy',
        'feeling', 'location',
        'reactions', 'comments',
        'shares', 'post',
        'created', 'updated'
    ]

    search_fields = [
        'user__username',
        'brand__slugname',
        'club__slugname',
        'privacy'
    ]

    list_filter = ['privacy']
    ordering = ['-created']

    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Comment model admin."""

    list_display = [
        'pk', 'author',
        'post', 'text',
        'reactions', 'type',
        'created', 'updated'
    ]

    search_fields = [
        'author__username',
        'post__pk'
    ]

    list_filter = ['type']
    ordering = ['-created']

    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False


@admin.register(PostReaction)
class ReactionPostAdmin(admin.ModelAdmin):
    """Reaction post model admin."""

    list_display = [
        'pk', 'user',
        'post', 'reaction',
        'created'
    ]

    search_fields = [
        'user__username',
        'post__pk'
    ]

    list_filter = ['reaction']

    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False


@admin.register(CommentReaction)
class ReactionCommentAdmin(admin.ModelAdmin):
    """Reaction comment model admin."""

    list_display = [
        'pk', 'user',
        'comment', 'reaction',
        'created'
    ]

    search_fields = [
        'comment__author__username'
    ]

    list_filter = ['reaction']

    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False
