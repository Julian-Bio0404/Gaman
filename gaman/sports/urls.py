"""Sports URLs"""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import ClubViewSet, LeagueViewSet, MemberViewSet


router = DefaultRouter()
router.register(r'leagues', LeagueViewSet, basename='leagues')
router.register(r'clubs', ClubViewSet, basename='clubs')
router.register(
    r'clubs/(?P<slugname>[a-zA-Z0-9_-]+)/members', MemberViewSet, basename='members')

urlpatterns = [path('', include(router.urls))]