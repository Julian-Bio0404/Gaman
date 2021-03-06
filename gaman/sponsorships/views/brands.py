"""Brands views."""

# Django
from django.db.models import Avg

# Django REST Framework
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


# Permissions
from rest_framework.permissions import IsAuthenticated
from gaman.sponsorships.permissions import (IsBrandOwner,
                                            IsProfileCompleted,
                                            IsSponsor)

# Models
from gaman.sponsorships.models import Brand, Rating
from gaman.users.models import FollowUp

# Serializers
from gaman.sponsorships.serializers import (BrandModelSerializer,
                                            CreateBrandSerializer)
                                           
from gaman.users.serializers import FollowerSerializer


class BrandViewSet(viewsets.ModelViewSet):
    """
    Brand viewset.
    Handle list, create, update, destroy
    retrieve and follow Brand.
    """

    queryset = Brand.objects.all()
    lookup_field = 'slugname'
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ('slugname',)
    ordering_fields = ('slugname',)
    ordering = ('slugname', 'created')
    filter_fields = ('verified',)

    def get_permissions(self):
        """Asign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions.append(IsBrandOwner)
        elif self.action in ['create']:
            permissions.append(IsProfileCompleted)
            permissions.append(IsSponsor)
        return [p() for p in permissions]

    def get_serializer_context(self):
        """Add sponsor to serializer context."""
        context = super(BrandViewSet, self).get_serializer_context()
        context['sponsor'] = self.request.user
        return context

    def get_serializer_class(self):
        """Return serializer based on action."""
        if self.action == 'create':
            return CreateBrandSerializer
        return BrandModelSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a brand and add rating average."""
        brand = self.get_object()
        rating = Rating.objects.filter(
            sponsorship__brand=brand).aggregate(Avg('rating'))
        data = BrandModelSerializer(brand).data
        data['rating'] = rating['rating__avg']
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def followers(self, request, *args, **kwargs):
        brand = self.get_object()
        followers = FollowUp.objects.filter(brand=brand)
        data = FollowerSerializer(followers, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def follow(self, request, *args, **kwarg):
        """Handle the follow-up to brand."""
        brand = self.get_object()
        follower = request.user
        followup = FollowUp.objects.filter(follower=follower, brand=brand)
        if followup.exists():
            followup.delete()
            data = {'message': 'You stopped follow to this brand.'}
            return Response(data, status=status.HTTP_200_OK)
        else:
            FollowUp.objects.create(follower=follower, brand=brand)
            data = {'message': 'You started follow to this brand.'}
            return Response(data=data, status=status.HTTP_201_CREATED)