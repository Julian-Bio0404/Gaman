"""Sports models admin."""

# Django
from django.contrib import admin

# Models
from gaman.sports.models import Club, Invitation, League, Member, SportEvent


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

    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    """League model admin."""

    fieldsets = (
        (None, {
            'fields': ('slugname', 'about', 'official_web', 'sport')
        }),
        ('Media', {
            'classes': ('extrapretty',),
            'fields': ('photo', 'cover_photo'),
        }),
        ('Site', {
            'classes': ('extrapretty',),
            'fields': ('country', 'state'),
        }),
    )

    list_display = [
        'pk', 'slugname',
        'about', 'country',
        'state', 'sport',
        'official_web',
        'created', 'updated'
    ]

    search_fields = [
        'slugname', 'country',
        'state', 'sport'
    ]

    list_filter = ['country', 'sport']

    def has_change_permission(self, request, obj=None) -> bool:
        return not Club.objects.filter(league=obj).exists()


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    """Invitation model admin."""

    list_display = [
        'id', 'issued_by', 'invited',
        'club', 'used'
    ]

    search_fields = [
        'issued_by__username',
        'invited__username',
        'club__slugname'
    ]

    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    """Member model admin."""

    list_display = [
        'user', 'club', 'active'
    ]

    search_fields = [
        'user__username', 'club__slugname'
    ]

    list_filter = ['active']

    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False


@admin.register(SportEvent)
class SportEventAdmin(admin.ModelAdmin):
    """SportEvent model admin."""

    list_display = [
        'pk', 'user', 'brand', 'club',
        'title', 'description',
        'photo', 'start', 'finish',
        'geolocation', 'country',
        'state', 'city', 'place',
        'created', 'updated'
    ]

    search_fields = [
        'user__username', 'club__slugname',
        'brand__slugname'
    ]

    list_filter = ['country', 'state']

    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False
