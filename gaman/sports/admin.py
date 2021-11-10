"""Sports models admin."""

# Django
from django.contrib import admin

# Models
from gaman.sports.models import Club, League


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    """Club model admin."""

    list_display = [
        'pk', 'league',
        'slugname', 'about', 'city',
        'trainer', 'official_web'
    ]

    search_fields = [
        'slugname', 'city',
        'league__slugname'
    ]
    
    list_filter = [
        'city', 'league__slugname'
    ]


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    """League model admin."""

    list_display = [
        'pk', 'slugname',
        'about', 'country',
        'state', 'sport',
        'official_web'
    ]

    search_fields = [
        'slugname', 'country',
        'state', 'sport'
    ]

    list_filter = [
        'country', 'state',
        'sport'
    ]