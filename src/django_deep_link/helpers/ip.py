import functools
import logging

import requests
from bs4 import BeautifulSoup
from django.conf import settings
from ipware import get_client_ip
from requests.exceptions import JSONDecodeError

logger = logging.getLogger(__name__)


@functools.lru_cache(maxsize=1024)
def get_ip_info(ip_address) -> dict:
    """
    Use 3rd party API to obtain Geolocation data from a given IP.

    Args:
        ip_address (str): The IP address to get information about.

    Returns:
        dict: A dictionary containing the information about the IP address,
        or an empty dictionary if the IP address is internal or the API response
        is not valid JSON.
    """
    if not ip_address or ip_address in settings.INTERNAL_IPS or ip_address.startswith("192.168."):
        logger.warning("IP address is internal: %s", ip_address)
        return {}

    def get_error_from_h1(response) -> str:
        soup = BeautifulSoup(response.text, "html.parser")
        h1_tag = soup.find("h1")
        return h1_tag.text if h1_tag else "No error message found"

    params = {
        "fields": "main",
        "hostname": 1,
        "access_key": settings.IPSTACK_ACCESS_KEY,
    }
    r = requests.get(f"https://api.ipstack.com/{ip_address}", params=params, timeout=5)
    r.raise_for_status()
    try:
        return r.json()
    except JSONDecodeError:
        error = get_error_from_h1(r)
        logger.warning("Could not decode JSON from IPStack API: %s", error)
        return {}


def get_ip(request) -> str:
    ip_address, _ = get_client_ip(request)
    return ip_address
