"""Comment serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from gaman.posts.models import Comment, Reply


class ReplyModelSerializer(serializers.ModelSerializer):
    """Reply model serializer."""

    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        """Meta options."""
        model = Reply
        fields = [
            'author', 'text', 
            'reactions', 'created'
        ]

        read_only_fields = [
            'author', 'reactions',
            'created'
        ]

    def create(self, data):
        """Create a comment reply."""
        author = self.context['author']
        post = self.context['post']
        comment = self.context['comment']

        # comment reply
        reply = Reply.objects.create(**data, author=author)

        # Update principal comment
        comment.replies.add(reply)
        comment.save()

        # Update Post
        post.comments += 1
        post.save()
        return reply


class CommentModelSerializer(serializers.ModelSerializer):
    """Comment model serializer."""

    author = serializers.StringRelatedField(read_only=True)
    
    replies = ReplyModelSerializer(
        read_only=True, required=False, many=True)

    class Meta:
        """Meta options."""
        model = Comment
        fields = [
            'author', 'text',
            'reactions', 'replies',
            'created'
        ]

        read_only_fields = [
            'author', 'reactions',
            'replies', 'created'
        ]

    def create(self, data):
        """Create a comment."""
        author = self.context['author']
        post = self.context['post']
        comment = Comment.objects.create(
            **data, author=author, post=post)

        # Update Post
        post.comments += 1
        post.save()
        return comment