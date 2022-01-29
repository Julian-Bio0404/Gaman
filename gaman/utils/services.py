"""Third services."""

# Utilities
import requests

# Django
from django.conf import settings


def get_ubication(place: str)-> dict:
    """
    Connection to HERE geocodification api.
    Determine country, state, city and geocodification (lat-lng) from a place name.
    """
    params = {'q': place, 'apiKey': settings.API_MAPS_KEY}
    response = requests.get(settings.API_MAPS_URL, params=params)

    place = response.json()['items'][0]['title']
    country = response.json()['items'][0]['address']['countryName']
    state = response.json()['items'][0]['address']['county']
    city = response.json()['items'][0]['address']['city']
    lat = response.json()['items'][0]['position']['lat']
    lng = response.json()['items'][0]['position']['lng']
    geolocation = f'{lat} {lng}'

    ubication = {
        'country': country, 'state': state,
        'city': city, 'place': place,
        'geolocation': geolocation
    }

    return ubication