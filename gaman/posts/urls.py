"""Posts URLs."""

# Django
from django.urls import include, path

# Django Rest Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import CommentViewSet, PostViewSet


router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')

router.register(
    r'posts/(?P<id>[0-9]+)/comments', CommentViewSet, basename='comments')

urlpatterns = [path('', include(router.urls))]
