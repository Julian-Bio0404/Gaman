"""sponsorships URLs."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import BrandViewSet, RatingViewSet, SponsorshipViewSet


router = DefaultRouter()
router.register(r'brands', BrandViewSet, basename='brands')
router.register(r'sponsorships', SponsorshipViewSet, basename='sponsorships')
router.register(
    r'sponsorships/(?P<id>[0-9]+)/ratings', RatingViewSet, basename='ratings')

urlpatterns = [
    path('', include(router.urls))
]