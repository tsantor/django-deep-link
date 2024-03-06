import pytest

from django_deep_link.models import App


@pytest.fixture
def ios_fixture():
    return {
        "name": "Twitter",
        "ios_app": True,
        "ios_bundle_id": "id333903271",
    }


@pytest.fixture
def android_fixture():
    return {
        "name": "Twitter",
        "android_app": True,
        "android_package_name": "com.twitter.android",
    }


@pytest.mark.django_db
class TestAppModel:

    @pytest.mark.django_db
    def test_get_app_store_url(self, ios_fixture):
        app = App.objects.create(**ios_fixture)
        assert app.get_app_store_url() == f"https://apps.apple.com/app/{ios_fixture['ios_bundle_id']}"

    def test_get_ios_redirect_url(self, ios_fixture):
        ios_fixture["ios_custom_url"] = "https://domain.com"
        app = App.objects.create(**ios_fixture)
        assert app.get_ios_redirect_url() == ios_fixture["ios_custom_url"]

    def test_get_ios_redirect_url_no_app(self):
        fixture = {
            "name": "Twitter",
            "ios_app": False,
            "ios_url": "https://domain.com/default",
        }
        app = App.objects.create(**fixture)
        assert app.get_ios_redirect_url() == fixture["ios_url"]

    def test_get_play_store_url(self, android_fixture):
        app = App.objects.create(**android_fixture)
        assert (
            app.get_play_store_url()
            == f"https://play.google.com/store/apps/details?id={android_fixture['android_package_name']}"
        )

    def test_get_android_redirect_url(self, android_fixture):
        android_fixture["android_custom_url"] = "https://domain.com"
        app = App.objects.create(**android_fixture)
        assert app.get_android_redirect_url() == android_fixture["android_custom_url"]

    def test_get_android_redirect_url_no_app(self):
        fixture = {
            "name": "Twitter",
            "android_app": False,
            "android_url": "htts://domain.com/no-android-app",
        }
        app = App.objects.create(**fixture)
        assert app.get_android_redirect_url() == fixture["android_url"]
