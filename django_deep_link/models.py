import uuid

import pytz
from django.conf import settings
from django.db.models import (
    CASCADE,
    CharField,
    ForeignKey,
    JSONField,
    UUIDField,
)
from django.urls import reverse
from model_utils.models import TimeStampedModel


class App(TimeStampedModel):
    """A deep link app."""

    code = UUIDField(default=uuid.uuid4, editable=False)

    name = CharField(max_length=255, help_text="The application display name.")

    # Android related settings
    android_package_name = CharField(
        max_length=255,
        help_text="com.company.appname",
        blank=True,
    )

    # iOS related settings
    apple_app_id = CharField(
        max_length=36,
        help_text="id1234567890",
        blank=True,
    )

    class Meta:
        ordering = ["android_package_name", "apple_app_id"]

    def __str__(self):
        return self.name

    @property
    def app_store_url(self):
        if self.apple_app_id:
            return f"https://apps.apple.com/app/{self.apple_app_id}"

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
