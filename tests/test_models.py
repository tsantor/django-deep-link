#!/usr/bin/env python

"""
test_django-deep-link
------------

Tests for `django-deep-link` models module.
"""

from django.test import TestCase

from django_deep_link import models


class Test_IOs(TestCase):
    """Test iOS related methods."""

    def setUp(self):
        pass

    def test_get_app_store_url(self):
        """App and bundle id."""
        fixture = {
            "name": "Twitter",
            "ios_app": True,
            "ios_bundle_id": "id333903271",
        }
        app = models.App.objects.create(**fixture)
        self.assertEqual(
            app.get_app_store_url(),
            f"https://apps.apple.com/app/{fixture['ios_bundle_id']}",
        )

    def test_get_ios_redirect_url(self):
        """App and custom url."""
        fixture = {
            "name": "Twitter",
            "ios_app": True,
            "ios_custom_url": "https://domain.com",
        }
        app = models.App.objects.create(**fixture)
        self.assertEqual(app.get_ios_redirect_url(), fixture["ios_custom_url"])

    def test_get_ios_redirect_url_no_app(self):
        """If no app, but a default URL."""
        fixture = {
            "name": "Twitter",
            "ios_app": False,
            "ios_url": "https://domain.com/default",
        }
        app = models.App.objects.create(**fixture)
        self.assertEqual(app.get_ios_redirect_url(), fixture["ios_url"])

    def tearDown(self):
        pass


class Test_Android(TestCase):
    """Test Android related methods."""

    def setUp(self):
        pass

    def test_get_play_store_url(self):
        """App and package name."""
        fixture = {
            "name": "Twitter",
            "android_app": True,
            "android_package_name": "com.twitter.android",
        }
        app = models.App.objects.create(**fixture)
        self.assertEqual(
            app.get_play_store_url(),
            f"https://play.google.com/store/apps/details?id={fixture['android_package_name']}",
        )

    def test_get_android_redirect_url(self):
        """App and custom url."""
        fixture = {
            "name": "Twitter",
            "android_app": True,
            "android_custom_url": "https://domain.com",
        }
        app = models.App.objects.create(**fixture)
        self.assertEqual(app.get_android_redirect_url(), fixture["android_custom_url"])

    def test_get_android_redirect_url_no_app(self):
        """If no app, but a default URL."""
        fixture = {
            "name": "Twitter",
            "android_app": False,
            "android_url": "htts://domain.com/no-android-app",
        }
        app = models.App.objects.create(**fixture)
        self.assertEqual(app.get_android_redirect_url(), fixture["android_url"])

    def tearDown(self):
        pass
