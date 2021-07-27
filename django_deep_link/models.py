import uuid
from django.db.models.fields import BooleanField
from django.utils.translation import gettext as _

import pytz
from django.conf import settings
from django.db.models import (
    CASCADE,
    CharField,
    ForeignKey,
    JSONField,
    UUIDField,
    URLField,
)
from django.urls import reverse
from model_utils.models import TimeStampedModel


class App(TimeStampedModel):
    """A deep link app."""

    code = UUIDField(default=uuid.uuid4, editable=False)

    name = CharField(max_length=255, help_text=_("The application display name."))

    default_url = URLField(
        _("Default URL"),
        help_text=_(
            "Your fallback URL for mobile devices that do not have a specified redirect."
        ),
    )

    # Android related settings ------------------------------------------------

    android_url = URLField(
        _("Android URL"),
        blank=True,
        help_text=_(
            "If blank, users will be redirected to the Default URL."
        ),
    )

    # If we have app, we hide the above field and use the below fields
    android_app = BooleanField(_("I have an Android App"), default=False)

    android_uri_scheme = CharField(
        _("Android URI Scheme"),
        max_length=255,
        help_text="myapp://",
        blank=True,
    )

    android_package_name = CharField(
        _("Android Package Name"),
        max_length=255,
        help_text="(e.g. - com.company.appname) If blank, users will be redirected to the Default URL",
        blank=True,
    )

    android_custom_url = URLField(
        _("Custom URL"),
        blank=True,
        help_text=_(
            "A URL to fallback to when the app is not installed."
        ),
    )

    # iOS related settings ----------------------------------------------------

    ios_url = URLField(
        _("iOS URL"),
        blank=True,
        help_text=_(
            "If blank, users will be redirected to the Default URL."
        ),
    )

    # If we have app, we hide the above field and use the below fields
    ios_app = BooleanField(_("I have an iOS App"), default=False)

    ios_uri_scheme = CharField(
        _("iOS URI Scheme"),
        max_length=255,
        help_text="myapp://",
        blank=True,
    )

    ios_bundle_id = CharField(
        _("iOS Bundle ID"),
        max_length=36,
        help_text="id1234567890",
        blank=True,
    )

    ios_custom_url = URLField(
        _("Custom URL"),
        blank=True,
        help_text=_(
            "A URL to fallback to when the app is not installed."
        ),
    )

    class Meta:
        ordering = ["android_package_name", "ios_bundle_id"]

    def __str__(self):
        return self.name

    @property
    def app_store_url(self):
        if self.ios_bundle_id:
            return f"https://apps.apple.com/app/{self.ios_bundle_id}"

    @property
    def play_store_url(self):
        if self.android_package_name:
            return f"https://play.google.com/store/apps/details?id={self.android_package_name}"

    def get_absolute_url(self):
        return reverse("django-deep-link:deep-link", kwargs={"code": self.code})


class Visit(TimeStampedModel):
    """A visit is any time a user visits the URL."""

    ip_address = CharField(blank=True, null=True, max_length=255, default="")
    ip_data = JSONField(
        "IP geodata",
        blank=True,
        null=True,
        default=dict,
        help_text="Must be valid JSON",
    )
    ua_data = JSONField(
        "User agent data",
        blank=True,
        null=True,
        default=dict,
        help_text="Must be valid JSON",
    )

    deep_link = ForeignKey(App, related_name="scans", on_delete=CASCADE)

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
        tz = pytz.timezone(settings.TIME_ZONE)
        dt = self.created.astimezone(tz)
        return f"{dt.strftime('%a %b %d, %Y at %-I:%M:%S %p')} from {self.ip_address}"
