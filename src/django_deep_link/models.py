import uuid

from django.db.models import CASCADE
from django.db.models import CharField
from django.db.models import ForeignKey
from django.db.models import JSONField
from django.db.models import Model
from django.db.models import URLField
from django.db.models import UUIDField
from django.db.models.fields import BooleanField
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _

from .mixins import IPAddressMixin
from .mixins import TimeStampedMixin
from .mixins import UserAgentMixin


class IOSMobileMixin(Model):
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

    def __str__(self):
        return self.ios_bundle_id

    def get_ios_redirect_url(self):
        """Return a redirect URL."""
        if not self.ios_app and self.ios_url:
            return self.ios_url
        if self.ios_app and self.ios_custom_url:
            return self.ios_custom_url
        return None


class AndroidMobileMixin(Model):
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

    def __str__(self):
        return self.android_package_name

    def get_play_store_url(self):
        if self.android_app and self.android_package_name:
            return f"https://play.google.com/store/apps/details?id={self.android_package_name}"
        return None


class MacDesktopMixin(Model):
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
        return None


class WindowsDesktopMixin(Model):
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
        return None


class App(
    IOSMobileMixin,
    AndroidMobileMixin,
    MacDesktopMixin,
    WindowsDesktopMixin,
    TimeStampedMixin,
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
        return str(self.name)

    def get_absolute_url(self):
        return reverse("django-deep-link:deep-link", kwargs={"code": self.code})


class Visit(UserAgentMixin, IPAddressMixin, TimeStampedMixin):
    """A visit is any time a user visits the URL."""

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

    def __str__(self):
        tz = timezone.get_current_timezone()
        dt = self.created_at.astimezone(tz)
        return f"{dt.strftime('%a %b %d, %Y at %-I:%M:%S %p')} from {self.ip_address}"
