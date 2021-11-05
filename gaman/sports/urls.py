"""Sports URLs"""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import ClubViewSet, LeagueListView, LeagueDetailView


router = DefaultRouter()
router.register(r'clubs', ClubViewSet, basename='clubs')

urlpatterns = [
    path('leagues/', LeagueListView.as_view(), name='leagues'),
    path('leagues/<str:slugname>/', LeagueDetailView.as_view(), name='league-detail'),
    path('', include(router.urls)),

]