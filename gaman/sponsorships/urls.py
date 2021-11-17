"""sponsorships URLs."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import BrandViewSet, RatingViewSet, SponsorshipViewSet, BrandPostViewSet


router = DefaultRouter()
router.register(r'brands', BrandViewSet, basename='brands')
router.register(r'sponsorships', SponsorshipViewSet, basename='sponsorships')

router.register(
    r'sponsorships/(?P<id>[0-9]+)/ratings', RatingViewSet, basename='ratings')

router.register(
    r'brands/(?P<slugname>[a-zA-Z0-9_-]+)/posts', BrandPostViewSet, basename='brand_posts')


urlpatterns = [
    path('', include(router.urls))
]