"""Reactions serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from gaman.posts.models import CommentReaction, PostReaction
from gaman.posts.models import ReplyReaction


class PostReactionModelSerializer(serializers.ModelSerializer):
    """Post Reaction model serializer."""

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
        # Si la reaccion del usuario existe, esta se elimina
        if reaction.exists():
            reaction.delete()
            post.reactions -= 1
            post.save()
        else:
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
    """Comment reaction model serializer."""

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
        # Si la reaccion del usuario existe, esta se elimina
        if reaction.exists():
            reaction.delete()
            comment.reactions -= 1
            comment.save()
        # Si no existe, procede a crearse
        else:
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


class ReplyReactionModelSerializer(serializers.ModelSerializer):
    """Reply reaction model serializer."""

    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        """Meta options."""
        model = ReplyReaction
        fields = ['user', 'reaction']
        read_only_fields = ['user']

    def validate(self, data):
        """Verify that the user's reaction does not exist yet."""
        user = self.context['user']
        reply = self.context['reply']
        reaction = ReplyReaction.objects.filter(user=user, reply=reply)
        # Si la reaccion del usuario existe, esta se elimina
        if reaction.exists():
            reaction.delete()
            reply.reactions -= 1
            reply.save()
        # Si no existe, procede a crearse
        else:
            return data

    def create(self, data):
        """Create a reply reaction."""
        user = self.context['user']
        reply = self.context['reply']
        reaction = ReplyReaction.objects.create(
            **data, user=user, reply=reply)

        # Reply update
        reply.reactions += 1
        reply.save()
        return reaction