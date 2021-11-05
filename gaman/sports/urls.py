"""Sports URLs"""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import ClubViewSet, LeagueViewSet


router = DefaultRouter()
router.register(r'clubs', ClubViewSet, basename='clubs')
router.register(r'leagues', LeagueViewSet, basename='leagues')

urlpatterns = [path('', include(router.urls))]