"""Club posts views."""

# Django REST framework
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

# Models
from gaman.sports.models import Club

# Serializers
from gaman.posts.serializers import PostModelSerializer


class ClubPostViewSet(viewsets.ModelViewSet):
    """Club Post viewset."""

    serializer_class = PostModelSerializer

    def dispatch(self, request, *args, **kwargs):
        """Verify that the brand exists."""
        slugname = kwargs['slugname']
        self.club = get_object_or_404(Club, slugname=slugname)
        return super(ClubPostViewSet, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Filter brand's posts."""
        return self.club.post_set.all()
    
    def get_serializer_context(self):
        """Add brand to serializer context."""
        context = super(ClubPostViewSet, self).get_serializer_context()
        context['author'] = self.club
        return context