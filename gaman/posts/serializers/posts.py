"""Posts serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from gaman.posts.models import Picture, Post, Video

# Serializers
from gaman.posts.serializers import ImageModelSerializer, VideoModelSerializer


class PostModelSerializer(serializers.ModelSerializer):
    """Post model serializer."""

    author = serializers.StringRelatedField(read_only=True)

    pictures = ImageModelSerializer(read_only=True, many=True)
    videos = VideoModelSerializer(read_only=True, many=True)

    tag_friends = serializers.StringRelatedField(many=True)

    class Meta:
        """Meta options."""
        model = Post
        fields = [
            'author','about',
            'privacy', 'location',
            'feeling', 'pictures',
            'videos', 'tag_friends',
            'reactions', 'comments',
            'shares',
        ]

        read_only_fields = [
            'author', 'pictures', 
            'videos', 'post',
            'reactions', 'comments', 
            'shares'
        ]
    
    def create(self, data):
        """Create a post."""
        author = self.context['author']
        post = Post.objects.create(**data, author=author)

        try:
            pictures = self.context['request'].data.getlist('pictures')
            videos = self.context['request'].data.getlist('videos')
            
            for img in pictures:
                picture = Picture.objects.create(content=img)
                post.pictures.add(picture)
                
            for i in videos:
                video = Video.objects.create(content=i)
                post.videos.add(video)
        except AttributeError:
            pass
        post.save()
        return post


class SharePostSerializer(serializers.ModelSerializer):
    """Share Post serializer."""

    author = serializers.StringRelatedField(read_only=True)
    post = PostModelSerializer(read_only=True, required=False)

    class Meta:
        """Meta options."""
        model = Post
        fields = [
            'author','about',
            'privacy', 'location',
            'feeling', 'post',
            'reactions', 'comments',
            'shares',
        ]

        read_only_fields = [
            'author', 'post',
            'reactions', 'comments', 
            'shares'
        ]

    def create(self, data):
        """Create a post."""
        author = self.context['author']
        repost = self.context['post']
        post = Post.objects.create(**data, author=author, post=repost)