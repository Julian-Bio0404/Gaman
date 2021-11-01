"""Sponsorships model admin."""

# Django
from django.contrib import admin

# models
from gaman.sponsorships.models import Brand, Rating, Sponsorship


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """Brand model admin."""

    list_display = [
        'pk', 'slugname',
        'photo', 'cover_photo',
        'about', 'official_web',
        'verified'
    ]

    search_fields = ['slugname', 'verified']
    list_filter = ['verified']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Rating model admin."""

    list_display = [
        'pk', 'sponsorship', 'qualifier',
        'comment', 'rating'
    ]

    search_fields = [
        'sponsorship__sponsor__username',
        'qualifier__username'
    ]

    list_filter = [
        'sponsorship__sponsor__username',
        'qualifier__username'
    ]


@admin.register(Sponsorship)
class SponsorshipAdmin(admin.ModelAdmin):
    """Sponsorship model admin."""

    list_display = [
        'pk', 'sponsor', 'athlete',
        'club', 'brand',
        'start', 'finish',
        'active'
    ]

    search_fields = [
        'sponsor__username',
        'athlete__username',
        'club__slugname',
        'brand__slugname', 'active'
    ]

    list_filter = [
        'sponsor__username',
        'athlete__username',
        'club__slugname',
        'brand__slugname', 'active'
    ]