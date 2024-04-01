from django.db import models
from django.test import TestCase

from django_deep_link.mixins import UserAgentMixin


class FakeModel(UserAgentMixin, models.Model):
    """Fake model for testing UserAgentMixin."""

    class Meta:
        abstract = False
        app_label = "fake_app"


class TestUserAgentMixin(TestCase):
    def setUp(self):
        self.mixin = FakeModel()
        self.mixin.ua_data = {
            "browser": {"family": "Chrome Mobile", "version_string": "89.0"},
            "os": {"family": "Android", "version_string": "10"},
            "device": {"brand": "Samsung", "family": "Galaxy"},
            "platform": "mobile",
        }

    def test_browser(self):
        assert self.mixin.browser == "Chrome Mobile"

    def test_browser_version(self):
        assert self.mixin.browser_version == "Chrome Mobile 89.0"

    def test_os(self):
        assert self.mixin.os == "Android"

    def test_os_version(self):
        assert self.mixin.os_version == "Android 10"

    def test_device(self):
        assert self.mixin.device == "Samsung"

    def test_device_family(self):
        assert self.mixin.device_family == "Samsung Galaxy"

    def test_platform(self):
        assert self.mixin.platform == "Mobile"
