"""Posts serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from gaman.posts.models import Picture, Post, Video
from gaman.users.models import User

# Serializers
from gaman.posts.serializers import ImageModelSerializer, VideoModelSerializer

# Utils
from gaman.utils.posts import PostAuthorContext


class PostSumaryModelSerializer(serializers.ModelSerializer):
    """
    Post Sumary model serializer.
    It's util for serialize post nested in other post (repost).
    """

    author = serializers.StringRelatedField(
        read_only=True, source='specify_author')

    pictures = ImageModelSerializer(read_only=True, many=True)
    videos = VideoModelSerializer(read_only=True, many=True)

    class Meta:
        """Meta options."""
        model = Post
        fields = [
            'author', 'about',
            'location', 'feeling',
            'pictures', 'videos',
            'created'
        ]

        read_only_fields = [
            'author', 'pictures',
            'videos', 'created'
        ]


class PostModelSerializer(PostSumaryModelSerializer):
    """
    Post model serializer.
    Handles the creation of user post.
    """
    author = serializers.StringRelatedField(
        read_only=True, source='specify_author')

    post = PostSumaryModelSerializer(read_only=True, required=False)

    tag_users = serializers.ListSerializer(
        required=False, child=serializers.CharField())

    class Meta:
        """Meta options."""
        model = Post
        fields = [
            'pk', 'author', 'about',
            'privacy', 'location',
            'feeling', 'pictures',
            'videos', 'tag_users',
            'post', 'reactions',
            'comments', 'shares',
            'created'
        ]

        read_only_fields = [
            'author', 'pictures',
            'videos', 'tag_users',
            'post', 'reactions',
            'comments', 'shares',
            'created'
        ]

    def validate(self, data):
        """Verify tag friends."""
        tag_users = data.get('tag_users', None)
        if tag_users:
            self.context['users'] = User.objects.filter(username__in=tag_users)
            data.pop('tag_users')
        return data

    def create(self, data):
        """Create a post."""
        author = self.context['author']
        post = PostAuthorContext.create_post(data, author)

        pictures = self.context['request'].data.getlist('pictures', None)
        videos = self.context['request'].data.getlist('videos', None)

        if pictures:
            pictures = Picture.objects.bulk_create(
                [Picture(content=img) for img in pictures])
            post.pictures.set(pictures)

        if videos:
            videos = Video.objects.bulk_create(
                [Video(content=video) for video in videos])
            post.videos.set(videos)

        # Add users tagged
        users = self.context.get('users', None)
        if users:
            post.tag_users.set(users)
        return post


class SharePostSerializer(serializers.ModelSerializer):
    """
    Share Post serializer.
    It's util when requesting user wants share a post.
    """

    author = serializers.StringRelatedField(
        read_only=True, source='specify_author')
    post = PostSumaryModelSerializer(read_only=True)

    class Meta:
        """Meta options."""
        model = Post
        fields = [
            'author', 'about',
            'privacy', 'location',
            'feeling', 'post',
            'reactions', 'comments',
            'shares', 'created'
        ]

        read_only_fields = [
            'author', 'post',
            'reactions', 'comments',
            'shares', 'created'
        ]

    def create(self, data):
        """Create a post."""
        post = Post.objects.create(
            **data, user=self.context['author'], post=self.context['post'])
        return post
