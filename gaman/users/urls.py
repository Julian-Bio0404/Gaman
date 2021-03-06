"""Users URLs."""

#Django
from django.urls import path, include

# Django Rest Framework
from rest_framework.routers import DefaultRouter

#Views
from .views import UserViewSet, ProfileViewSet, FollowRequestViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'profiles', ProfileViewSet, basename='profiles')

router.register(
    r'profiles/(?P<username>[a-zA-Z0-9]+)/requests', 
    FollowRequestViewSet, basename='follow_requests')

urlpatterns = [
    path('', include(router.urls))
]