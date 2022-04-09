"""Third services."""

# Utilities
import requests

# Django
from django.conf import settings


def get_ubication(place: str) -> dict:
    """
    Connection to HERE geocodification api.
    Determine country, state, city and 
    geocodification (lat-lng) from a place name.
    """
    params = {'q': place, 'apiKey': settings.API_MAPS_KEY}
    response = requests.get(settings.API_MAPS_URL, params=params)
    response = response.json()['items'][0]

    place = response['title']
    country = response['address']['countryName']
    state = response['address']['county']
    city = response['address']['city']
    lat = response['position']['lat']
    lng = response['position']['lng']

    ubication = {
        'country': country, 'state': state,
        'city': city, 'place': place,
        'geolocation': f'{lat} {lng}'
    }
    return ubication
