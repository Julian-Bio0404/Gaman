"""Sports URLs"""

# Django
from django.urls import path

# Views
from .views import LeagueListView, LeagueDetailView


urlpatterns = [
    path('leagues/', LeagueListView.as_view(), name='leagues'),
    path('leagues/<str:slugname>/', LeagueDetailView.as_view(), name='league-detail')
]