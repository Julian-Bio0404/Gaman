"""Gaman URL Configuration."""

# Django
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path(r'auth/', include('rest_framework_social_oauth2.urls')),
    path('', include(('gaman.users.urls', 'users'), namespace='users')),
    path('', include(('gaman.posts.urls', 'posts'), namespace='posts')),
    path('', include(('gaman.sponsorships.urls', 'sponsorships'), namespace='sponsorships')),
    path('', include(('gaman.sports.urls', 'sports'), namespace='sports')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)