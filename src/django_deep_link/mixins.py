# from django.conf import settings
from dataclasses import dataclass

from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserAgentMixin(models.Model):
    """Model mixin which provides us with user agent data."""

    ua_data = models.JSONField(
        _("User Agent Data"),
        blank=True,
        null=True,
        default=dict,
        help_text="Must be valid JSON",
    )

    class Meta:
        abstract = True

    @property
    def browser(self) -> str:
        """Normalize browser family."""
        if data := self.ua_data.get("browser"):
            if browser := data.get("family"):
                if "Mobile Safari" in browser:
                    return "Mobile Safari"
                elif "Chrome Mobile" in browser:
                    return "Chrome Mobile"
                return browser

    @property
    def browser_version(self) -> str:
        data = self.ua_data.get("browser")
        return f'{self.browser} {data.get("version_string")}' if data else ""

    @property
    def os(self) -> str:
        data = self.ua_data.get("os")
        return data.get("family") if data else ""

    @property
    def os_version(self) -> str:
        data = self.ua_data.get("os")
        return f'{data.get("family")} {data.get("version_string")}' if data else ""

    @property
    def device(self) -> str:
        """Normalize device brand."""
        if data := self.ua_data.get("device"):
            if brand := data.get("brand", ""):
                return "Generic" if "Generic" in brand else brand

    @property
    def device_family(self) -> str:
        """Return device family."""
        if data := self.ua_data.get("device"):
            brand = data.get("brand")
            family = data.get("family")
            if brand and family and brand in family:
                return data.get("family")
            elif brand and family:
                return f'{data.get("brand")} {data.get("family")}'

    @property
    def platform(self) -> str:
        platform = self.ua_data.get("platform")
        return platform.title() if platform else ""


@dataclass
class IPAddressData:
    ip: str
    zip: str
    city: str
    type: str
    latitude: float
    longitude: float
    region_code: str
    region_name: str
    country_code: str
    country_name: str
    continent_code: str
    continent_name: str


class IPAddressMixin(models.Model):
    """Model mixin which provides IP data."""

    ip_address = models.CharField(_("IP Address"), blank=True, null=True, max_length=255, default="")
    ip_data = models.JSONField(
        _("IP Data"),
        blank=True,
        null=True,
        default=dict,
        help_text="Must be valid JSON",
    )

    class Meta:
        abstract = True

    def ip_parsed(self) -> IPAddressData:
        """Return IP data as a dataclass."""
        if self.ip_data:
            return IPAddressData(**self.ip_data)

    # def ip(self) -> str:
    #     self.ip_data.get("ip")

    @property
    def location(self) -> str:
        city = self.ip_data.get("city")
        state = self.ip_data.get("region_code")
        country = self.ip_data.get("country_name")
        if city and state and country:
            return f"{city}, {state} ({country})"
