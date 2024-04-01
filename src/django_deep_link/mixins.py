from django.db import models
from django.utils.translation import gettext_lazy as _

from .dtos import IPAddressData


class TimeStampedMixin(models.Model):
    """Model mixin which provides us with created_at and updated_at fields."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserAgentMixin(models.Model):
    """Model mixin which provides us with user agent data."""

    ua_data = models.JSONField(
        _("User Agent Data"),
        blank=True,
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
                if "Chrome Mobile" in browser:
                    return "Chrome Mobile"
                return browser
        return ""

    @property
    def browser_version(self) -> str:
        """Normalize browser version."""
        data = self.ua_data.get("browser")
        return f'{self.browser} {data.get("version_string")}' if data else ""

    @property
    def os(self) -> str:
        """Normalize OS family."""
        data = self.ua_data.get("os")
        return data.get("family") if data else ""

    @property
    def os_version(self) -> str:
        """Normalize OS version."""
        data = self.ua_data.get("os")
        return f'{data.get("family")} {data.get("version_string")}' if data else ""

    @property
    def device(self) -> str:
        """Normalize device brand."""
        if data := self.ua_data.get("device"):
            if brand := data.get("brand", ""):
                return "Generic" if "Generic" in brand else brand
        return ""

    @property
    def device_family(self) -> str:
        """Return device family."""
        if data := self.ua_data.get("device"):
            brand = data.get("brand")
            family = data.get("family")
            if brand and family and brand in family:
                return data.get("family")
            return f'{data.get("brand")} {data.get("family")}'
        return ""

    @property
    def platform(self) -> str:
        """Normalize platform."""
        platform = self.ua_data.get("platform")
        return platform.title() if platform else ""


class IPAddressMixin(models.Model):
    """Model mixin which provides IP data."""

    ip_address = models.CharField(
        _("IP Address"),
        blank=True,
        max_length=255,
        default="",
    )
    ip_data = models.JSONField(
        _("IP Data"),
        blank=True,
        default=dict,
        help_text="Must be valid JSON",
    )

    class Meta:
        abstract = True

    def ip_parsed(self) -> IPAddressData:
        """Return IP data as a dataclass."""
        if self.ip_data:
            return IPAddressData(**self.ip_data)
        return IPAddressData()

    @property
    def location(self) -> str:
        """Return location string."""
        city = self.ip_data.get("city")
        state = self.ip_data.get("region_code")
        country = self.ip_data.get("country_name")
        if city and state and country:
            return f"{city}, {state} ({country})"
        return ""
