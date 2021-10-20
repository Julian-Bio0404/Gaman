"""Posts models admin."""

# Django
from django.contrib import admin

# Models
from gaman.posts.models import Comment, CommentReaction, Post, PostReaction


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Post model admin."""

    list_display = [
        'pk','author',
        'about', 'privacy',
        'feeling', 'location', 
        'reactions', 'comments',
        'shares', 'post',
        'created', 'updated'
    ]

    search_fields = [
        'author__username', 
        'location', 'privacy'
    ]

    list_filter = [
        'author__username',
        'location', 'privacy'
    ]

    ordering = ['-created']


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
        'post', 'type'
    ]

    list_filter = [
        'author__username',
        'post', 'type'
    ]

    ordering = ['-created']


@admin.register(PostReaction)
class ReactionPostAdmin(admin.ModelAdmin):
    """Reaction post model admin."""

    list_display = [
        'pk', 'user',
        'post', 'reaction',
        'created'
    ]

    search_fields = ['post']
    list_filter = ['post']


@admin.register(CommentReaction)
class ReactionCommentAdmin(admin.ModelAdmin):
    """Reaction comment model admin."""

    list_display = [
        'pk', 'user',
        'comment', 'reaction',
        'created'
    ]

    search_fields = ['comment']
    list_filter = ['comment']