"""Club serializers."""

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Models
from gaman.sports.models import Club, League


class ClubModelSerializer(serializers.ModelSerializer):
    """Club model serializer."""

    league = serializers.StringRelatedField(read_only=True)
    trainer = serializers.StringRelatedField(read_only=True)

    class Meta:
        """Meta options."""
        model = Club
        fields = [
            'slugname', 'league',
            'about', 'photo',
            'cover_photo', 'city',
            'trainer', 'official_web'
        ]

        read_only_fields = [
            'league', 'trainer',
            'slugname'
        ]


class CreateClubSerializer(serializers.Serializer):
    """
    Create Club Serializer.
    Handle the creation of a club.
    """

    league = serializers.CharField(min_length=3, max_length=40, required=False)

    slugname = serializers.SlugField(
        min_length=3, max_length=40,
        validators=[UniqueValidator(queryset=Club.objects.all())])

    about = serializers.CharField(min_length=20, max_length=250, required=False)

    official_web = serializers.URLField(required=False)
    photo = serializers.ImageField(required=False)
    cover_photo = serializers.ImageField(required=False)

    city = serializers.CharField(min_length=3, max_length=60, required=False)

    def validate(self, data):
        """Verify that league exists."""
        league_slugname = data.get('league', None)
        if league_slugname:
            try:
                league = League.objects.get(slugname=league_slugname)
                self.context['league'] = league
                data.pop('league')
            except League.DoesNotExist:
                raise serializers.ValidationError(
                    'The League does not exists.')
        return data

    def create(self, data):
        """Create a Club."""
        trainer = self.context['trainer']
        league = self.context.get('league', None)
        club = Club.objects.create(**data, trainer=trainer, league=league)
        return club
