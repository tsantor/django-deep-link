import logging

import requests
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)


def get_ip_geodata(ip_address):
    """Use 3rd party API to obtain Geolocation data from a given IP."""

    if ip_address in settings.INTERNAL_IPS:
        logger.debug(
            "Not looking up IP gelocation data, IP is is found in INTERNAL_IPS"
        )
        return {}

    if cache.get(ip_address):
        return cache.get(ip_address)

    if not hasattr(settings, 'IPSTACK_ACCESS_KEY'):
        logger.warn(
            "Unable to lookup IP geolocation data, IPSTACK_ACCESS_KEY not in settings"
        )
        return {}

    params = {
        "fields": "main",
        "hostname": 1,
        "access_key": settings.IPSTACK_ACCESS_KEY,
    }
    r = requests.get(f"https://api.ipstack.com/{ip_address}", params=params)
    r.raise_for_status()
    cache.set(ip_address, r.json(), settings.IPSTACK_CACHE_TIME)
    return r.json()
