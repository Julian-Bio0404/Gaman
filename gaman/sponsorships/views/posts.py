"""Brand posts views."""

# Django REST framework
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

# Models
from gaman.sponsorships.models import Brand

# Serializers
from gaman.posts.serializers import PostModelSerializer


class BrandPostViewSet(viewsets.ModelViewSet):
    """Brand Post viewset."""

    serializer_class = PostModelSerializer

    def dispatch(self, request, *args, **kwargs):
        """Verify that the brand exists."""
        slugname = kwargs['slugname']
        self.brand = get_object_or_404(Brand, slugname=slugname)
        return super(BrandPostViewSet, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Filter brand's posts."""
        return self.brand.post_set.all()
    
    def get_serializer_context(self):
        """Add brand to serializer context."""
        context = super(BrandPostViewSet, self).get_serializer_context()
        context['author'] = self.brand
        return context