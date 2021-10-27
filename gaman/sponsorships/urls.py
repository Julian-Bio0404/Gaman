"""Brands URLs."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import BrandViewSet


router = DefaultRouter()
router.register(r'brands', BrandViewSet, basename='brands')

urlpatterns = [
    path('', include(router.urls))
]