"""Sports URLs"""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import (ClubPostViewSet, ClubViewSet,
                    LeagueViewSet, MemberViewSet,
                    SportEventClubViewSet,
                    SportEventViewSet)


router = DefaultRouter()
router.register(r'leagues', LeagueViewSet, basename='leagues')
router.register(r'clubs', ClubViewSet, basename='clubs')
router.register(r'events', SportEventViewSet, basename='events')

router.register(
    r'clubs/(?P<slugname>[a-zA-Z0-9_-]+)/members', MemberViewSet, basename='members')

router.register(
    r'clubs/(?P<slugname>[a-zA-Z0-9_-]+)/events', SportEventClubViewSet, basename='club-events')

router.register(
    r'clubs/(?P<slugname>[a-zA-Z0-9_-]+)/posts', ClubPostViewSet, basename='club-posts')


urlpatterns = [path('', include(router.urls))]
