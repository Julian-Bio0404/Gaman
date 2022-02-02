"""Club posts views."""

# Django REST framework
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404

# Permissions
from rest_framework.permissions import IsAuthenticated
from gaman.sports.permissions import IsClubOwner

# Models
from gaman.sports.models import Club

# Serializers
from gaman.posts.serializers import PostModelSerializer


class ClubPostViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    """Club Post viewset."""

    serializer_class = PostModelSerializer

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permissions = [IsAuthenticated, IsClubOwner]
        else:
            permissions = [IsAuthenticated]
        return[p() for p in permissions]

    def dispatch(self, request, *args, **kwargs):
        """Verify that the club exists."""
        slugname = kwargs['slugname']
        self.club = get_object_or_404(Club, slugname=slugname)
        return super(ClubPostViewSet, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Filter brand's posts."""
        return self.club.post_set.all()

    def get_serializer_context(self):
        """Add club to serializer context."""
        context = super(ClubPostViewSet, self).get_serializer_context()
        context['author'] = self.club
        return context