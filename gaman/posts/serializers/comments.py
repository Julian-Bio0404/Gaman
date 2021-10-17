"""Comment serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from gaman.posts.models import Comment


class CommentModelSerializer(serializers.ModelSerializer):
    """Comment model serializer."""

    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        """Meta options."""
        model = Comment
        fields = ['author', 'text', 'reactions']

        read_only_fields = [
            'author', 'reactions'
        ]

    def create(self, data):
        """Create a comment."""
        # comment
        author = self.context['author']
        post = self.context['post']
        comment = Comment.objects.create(
            **data, author=author, post=post)

        # Post
        post.comments += 1
        post.save()
        return comment


class ComentReplySerializer(CommentModelSerializer):
    """Comment Reply serializer."""

    def create(self, data):
        """Create a comment reply."""
        # comment reply
        author = self.context['author']
        post = self.context['post']
        comment = self.context['comment']
        comment = Comment.objects.create(
            **data, author=author, post=post, comment=comment)

        # Post
        post.comments += 1
        post.save()
        return comment