from dataclasses import dataclass


@dataclass
class IPAddressData:
    """Dataclass for IP data."""

    ip: str = ""
    zip: int = 0
    city: str = ""
    type: str = ""
    latitude: float = 0.0
    longitude: float = 0.0
    region_code: str = ""
    region_name: str = ""
    country_code: str = ""
    country_name: str = ""
    continent_code: str = ""
    continent_name: str = ""
