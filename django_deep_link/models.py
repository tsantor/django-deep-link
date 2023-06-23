import uuid
from zoneinfo import ZoneInfo

from django.conf import settings
from django.db.models import (
    CASCADE,
    CharField,
    ForeignKey,
    JSONField,
    Model,
    URLField,
    UUIDField,
)
from django.db.models.fields import BooleanField
from django.urls import reverse
from django.utils.translation import gettext as _

from django_deep_link.mixins import TimeStampedModel


class iosMobile(Model):
    """iOS Mobile related settings."""

    ios_url = URLField(
        _("iOS URL"),
        blank=True,
        help_text=_(
            "Custom app download/coming soon page. If blank, users will not be redirected."
        ),
    )

    # If we have app, we hide the above field and use the below fields
    ios_app = BooleanField(_("I have an iOS App"), default=False)

    ios_uri_scheme = CharField(
        _("iOS URI Scheme"),
        max_length=255,
        help_text=_("myapp://"),
        blank=True,
    )

    ios_bundle_id = CharField(
        _("iOS Bundle ID"),
        max_length=36,
        help_text=_("i.e. - id1234567890"),
        blank=True,
    )

    ios_custom_url = URLField(
        _("Custom URL"),
        blank=True,
        help_text=_("A URL to fallback to when the app is not installed."),
    )

    class Meta:
        abstract = True

    def get_app_store_url(self):
        if self.ios_app and self.ios_bundle_id:
            return f"https://apps.apple.com/app/{self.ios_bundle_id}"

    def get_ios_redirect_url(self):
        """Return a redirect URL."""
        if not self.ios_app and self.ios_url:
            return self.ios_url
        if self.ios_app and self.ios_custom_url:
            return self.ios_custom_url


class AndroidMobile(Model):
    """Android Mobile related settings."""

    android_url = URLField(
        _("Android URL"),
        blank=True,
        help_text=_(
            "Custom app download/coming soon page. If blank, users will not be redirected."
        ),
    )

    # If we have app, we hide the above field and use the below fields
    android_app = BooleanField(_("I have an Android App"), default=False)

    android_uri_scheme = CharField(
        _("Android URI Scheme"),
        max_length=255,
        help_text=_("i.e. - myapp://"),
        blank=True,
    )

    android_package_name = CharField(
        _("Android Package Name"),
        max_length=255,
        help_text=_(
            "i.e. - com.company.appname. If blank, users will be redirected to the Default URL"
        ),
        blank=True,
    )

    android_custom_url = URLField(
        _("Custom URL"),
        blank=True,
        help_text=_("A URL to fallback to when the app is not installed."),
    )

    class Meta:
        abstract = True

    def get_play_store_url(self):
        if self.android_app and self.android_package_name:
            return f"https://play.google.com/store/apps/details?id={self.android_package_name}"

    def get_android_redirect_url(self):
        """Return a redirect URL."""
        if not self.android_app and self.android_url:
            return self.android_url
        if self.android_app and self.android_custom_url:
            return self.android_custom_url


class MacDesktop(Model):
    """Mac Desktop related settings."""

    mac_app = BooleanField(_("I have a Mac App"), default=False)

    mac_uri_scheme = CharField(
        _("Mac URI Scheme"),
        max_length=255,
        help_text=_("i.e. - myapp://"),
        blank=True,
    )

    mac_app_store_url = URLField(
        _("Mac App Store URL"),
        max_length=255,
        help_text=_("A URL to fallback to when the app is not installed."),
        blank=True,
    )

    class Meta:
        abstract = True

    def get_mac_app_store_url(self):
        if self.mac_app and self.mac_app_store_url:
            return self.mac_app_store_url


class WindowsDesktop(Model):
    """Windows Desktop related settings."""

    windows_app = BooleanField(_("I have a Windows App"), default=False)

    windows_uri_scheme = CharField(
        _("Windows URI Scheme"),
        max_length=255,
        help_text=_("i.e. - myapp://"),
        blank=True,
    )

    windows_app_store_url = URLField(
        _("Windows App Store URL"),
        max_length=255,
        help_text=_("A URL to fallback to when the app is not installed."),
        blank=True,
    )

    windows_package_name = CharField(
        _("Windows Package Family Name"),
        max_length=36,
        # help_text=_(""),
        blank=True,
    )

    class Meta:
        abstract = True

    def get_windows_app_store_url(self):
        if self.windows_app and self.windows_app_store_url:
            return self.windows_app_store_url


class App(
    iosMobile, AndroidMobile, MacDesktop, WindowsDesktop, TimeStampedModel, Model
):
    """A deep link app."""

    code = UUIDField(default=uuid.uuid4, editable=False)

    name = CharField(max_length=255, help_text=_("The application display name."))

    default_url = URLField(
        _("Default URL"),
        help_text=_(
            "Your fallback URL for platforms that do not have a specified redirect."
        ),
    )

    class Meta:
        ordering = [
            "name",
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("django-deep-link:deep-link", kwargs={"code": self.code})


class Visit(TimeStampedModel):
    """A visit is any time a user visits the URL."""

    ip_address = CharField(blank=True, null=True, max_length=255, default="")
    ip_data = JSONField(
        _("IP geodata"),
        blank=True,
        default=dict,
    )
    ua_data = JSONField(
        _("User agent data"),
        blank=True,
        default=dict,
    )
    query_data = JSONField(
        _("Query data"),
        blank=True,
        default=dict,
    )

    deep_link = ForeignKey(App, related_name="scans", on_delete=CASCADE)

    class Meta:
        default_permissions = (
            "delete",
            "view",
        )

    @property
    def browser(self):
        data = self.ua_data.get("browser")
        return data.get("family", None) if data else None

    @property
    def os(self):
        data = self.ua_data.get("os")
        return data.get("family", None) if data else None

    @property
    def device(self):
        data = self.ua_data.get("device")
        return data.get("family", None) if data else None

    @property
    def platform(self):
        platform = self.ua_data.get("platform", None)
        return platform.title() if platform else None

    def __str__(self):
        tz = ZoneInfo(settings.TIME_ZONE)
        dt = self.created.astimezone(tz)
        return f"{dt.strftime('%a %b %d, %Y at %-I:%M:%S %p')} from {self.ip_address}"
