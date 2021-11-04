"""Reactions serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from gaman.posts.models import CommentReaction, PostReaction


class PostReactionModelSerializer(serializers.ModelSerializer):
    """
    Post Reaction model serializer.
    Handles the creation Post reaction.
    """

    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        """Meta options."""
        model = PostReaction
        fields = ['user', 'reaction']
        read_only_fields = ['user']

    def validate(self, data):
        """verify that the user's reaction does not exist yet."""
        user = self.context['user']
        post = self.context['post']
        reaction = PostReaction.objects.filter(user=user, post=post)
        # If the user's reaction exists, this is deleted
        if reaction.exists():
            reaction.delete()
            post.reactions -= 1
            post.save()
        return data

    def create(self, data):
        """Create a post reaction."""
        user = self.context['user']
        post = self.context['post']
        reaction = PostReaction.objects.create(**data, user=user, post=post)

        # Update Post
        post.reactions += 1
        post.save()
        return reaction


class CommentReactionModelSerializer(serializers.ModelSerializer):
    """
    Comment reaction model serializer.
    Handle the creation Comment reaction.
    """

    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        """Meta options."""
        model = CommentReaction
        fields = ['user', 'reaction']
        read_only_fields = ['user']

    def validate(self, data):
        """Verify that the user's reaction does not exist yet."""
        user = self.context['user']
        comment = self.context['comment']
        reaction = CommentReaction.objects.filter(user=user, comment=comment)
        # If the user's reaction exists, this is deleted
        if reaction.exists():
            reaction.delete()
            comment.reactions -= 1
            comment.save()
        return data

    def create(self, data):
        """Create a comment reaction."""
        user = self.context['user']
        comment = self.context['comment']
        reaction = CommentReaction.objects.create(
            **data, user=user, comment=comment)

        # Comment update
        comment.reactions += 1
        comment.save()
        return reaction