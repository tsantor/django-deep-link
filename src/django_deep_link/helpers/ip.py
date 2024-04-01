import functools
import ipaddress
import logging
from abc import ABC, abstractmethod

import requests
from django.conf import settings
from django.http import HttpRequest
from ipware import get_client_ip
from requests.exceptions import JSONDecodeError

logger = logging.getLogger(__name__)


class GeoLocationAPI(ABC):
    @abstractmethod
    def get_ip_info(self, ip_address: str) -> dict:
        pass


class IPStackAPI(GeoLocationAPI):
    def get_ip_info(self, ip_address: str) -> dict:
        params = {
            "fields": "main",
            "hostname": 1,
            "access_key": settings.IPSTACK_ACCESS_KEY,
        }
        r = requests.get(
            f"https://api.ipstack.com/{ip_address}",
            params=params,
            timeout=5,
        )
        r.raise_for_status()
        try:
            return r.json()
        except JSONDecodeError:
            return {}


@functools.lru_cache(maxsize=1024)
def get_ip_info(ip_address: str, api: GeoLocationAPI) -> dict:
    """
    Use 3rd party API to obtain Geolocation data from a given IP.

    Args:
        ip_address (str): The IP address to get information about.
        api (GeoLocationAPI): The API to use to get the IP info.

    Returns:
        dict: A dictionary containing the information about the IP address,
              or an empty dictionary if the IP address is internal or the API
              response is not valid JSON.
    """
    if (
        not ip_address
        or ip_address in settings.INTERNAL_IPS
        or is_private_ip(ip_address)
    ):
        # logger.warning("IP address is internal: %s", ip_address)
        return {}

    try:
        return api.get_ip_info(ip_address)
    except Exception as e:  # noqa: BLE001
        logger.warning("Could not get IP info from API: %s", str(e))
        return {}


def get_ip(request: HttpRequest) -> str:
    """
    This function retrieves the client's IP address from the request.

    Args:
        request (HttpRequest): The request object.

    Returns:
        str: The IP address of the client.
    """
    ip_address, _ = get_client_ip(request)
    return ip_address


def is_private_ip(ip_address: str) -> bool:
    """
    This function checks if the given IP address is private.

    Args:
        ip_address (str): The IP address to check.

    Returns:
        bool: True if the IP address is private, False otherwise.
    """
    try:
        return ipaddress.ip_address(ip_address).is_private
    except ValueError:
        logger.warning("Invalid IP address: %s", ip_address)
        return False
