import requests
from django.conf import settings
from django.core.cache import cache
from ipware import get_client_ip

def get_ip_from_request(request):
    """
    Get the client IP in order of priority.  This is not guaranteed and
    can be easily spoofed.

    https://en.wikipedia.org/wiki/X-Forwarded-For
    """
    # meta = request.META

    # if "HTTP_X_FORWARDED_FOR" in meta and meta.get("HTTP_X_FORWARDED_FOR") != "":
    #     # The first obtained IP address is the real IP address of the client
    #     return meta.get("HTTP_X_FORWARDED_FOR").split(",")[0]
    # elif "HTTP_X_REAL_IP" in meta and meta.get("HTTP_X_REAL_IP") != "":
    #     return meta.get("HTTP_X_REAL_IP")
    # elif "REMOTE_ADDR" in meta and meta.get("REMOTE_ADDR") != "":
    #     return meta.get("REMOTE_ADDR")

    # In a view or a middleware where the `request` object is available
    client_ip, is_routable = get_client_ip(request)
    if client_ip:
        # We got the client's IP address
        return client_ip
        # if is_routable:
            # The client's IP address is publicly routable on the Internet
        # else:
            # The client's IP address is private
    # else:
        # Unable to get the client's IP address

    # Order of precedence is (Public, Private, Loopback, None)


def get_ip_address_information(ip_address):
    """Use 3rd party API to obtain Geolocation data from a given IP."""
    if ip_address in settings.INTERNAL_IPS:
        # print(settings.INTERNAL_IPS)
        return {}

    if not cache.get(ip_address):
        params = {
            "fields": "main",
            "hostname": 1,
            "access_key": settings.IPSTACK_ACCESS_KEY,
        }
        r = requests.get(f"https://api.ipstack.com/{ip_address}", params=params)
        r.raise_for_status()
        cache.set(ip_address, r.json(), settings.IPSTACK_CACHE_TIME)
        return r.json()

    return cache.get(ip_address)
