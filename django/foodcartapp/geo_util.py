import requests
from django.db.utils import IntegrityError
from django.utils.timezone import now, localtime
from geopy.distance import distance
from geopy.geocoders import Yandex
from location.models import Location
from django.conf import settings


API_KEY = settings.YANDEX_GEOCODER_API_KEY


def fetch_coordinates(apikey, address):

    yandex_geocoder = Yandex(apikey)
    location = yandex_geocoder.geocode(address)

    if location:
        lat = location.latitude
        lon = location.longitude
    else:
        lat = 0.0
        lon = 0.0

    try:
        Location.objects.create(
            address=address,
            lon=lon,
            lat=lat,
            updated_at=localtime(now())
        )
    except IntegrityError:
        pass

    return lat, lon


def check_location(lat, lon, address):
    if not lat and not lon:
        lat, lon = fetch_coordinates(API_KEY, address)

    return lat, lon


def calculate_distance(order_location, rest_location):
    if order_location and rest_location:
        return round(distance(order_location, rest_location).km, 1)
