"""Brands URLs."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import BrandViewSet, SponsorshipViewSet


router = DefaultRouter()
router.register(r'brands', BrandViewSet, basename='brands')
router.register(r'sponsorships', SponsorshipViewSet, basename='sponsorships')

urlpatterns = [
    path('', include(router.urls))
]