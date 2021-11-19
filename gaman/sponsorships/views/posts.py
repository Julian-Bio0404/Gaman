"""Brand posts views."""

# Django REST framework
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

# Permissions
from rest_framework.permissions import IsAuthenticated
from gaman.sponsorships.permissions import IsBrandOwner

# Models
from gaman.sponsorships.models import Brand

# Serializers
from gaman.posts.serializers import PostModelSerializer


class BrandPostViewSet(viewsets.ModelViewSet):
    """Brand Post viewset."""

    serializer_class = PostModelSerializer

    def get_permissions(self):
        """Asign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            print(self.action)
            permissions.append(IsBrandOwner)
        return [p() for p in permissions]

    def dispatch(self, request, *args, **kwargs):
        """Verify that the brand exists."""
        self.brand = get_object_or_404(Brand, slugname=kwargs['slugname'])
        return super(BrandPostViewSet, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Filter brand's posts."""
        return self.brand.post_set.all()
    
    def get_serializer_context(self):
        """Add brand to serializer context."""
        context = super(BrandPostViewSet, self).get_serializer_context()
        context['author'] = self.brand
        return context