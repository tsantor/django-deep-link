import pytest
from django.db import models
from django_deep_link.dtos import IPAddressData
from django_deep_link.mixins import IPAddressMixin
from django_deep_link.mixins import UserAgentMixin


class FakeModel(UserAgentMixin, IPAddressMixin, models.Model):
    """Fake model for testing UserAgentMixin."""

    class Meta:
        abstract = False
        app_label = "fake_app"

    def __str__(self):
        return "Fake Model"


@pytest.fixture()
def user_agent_mixin():
    mixin = FakeModel()
    mixin.ua_data = {
        "browser": {"family": "Chrome Mobile", "version_string": "89.0"},
        "os": {"family": "Android", "version_string": "10"},
        "device": {"brand": "Samsung", "family": "Galaxy"},
        "platform": "mobile",
    }
    return mixin


def test_user_agent_mixin(user_agent_mixin):
    assert user_agent_mixin.browser == "Chrome Mobile"
    assert user_agent_mixin.browser_version == "Chrome Mobile 89.0"
    assert user_agent_mixin.os == "Android"
    assert user_agent_mixin.os_version == "Android 10"
    assert user_agent_mixin.device == "Samsung"
    assert user_agent_mixin.device_family == "Samsung Galaxy"
    assert user_agent_mixin.platform == "Mobile"


@pytest.fixture()
def ip_address_mixin():
    mixin = FakeModel()
    mixin.ip_address = "99.70.213.72"
    mixin.ip_data = {
        "ip": "99.70.213.72",
        "zip": "32819",
        "city": "Orlando",
        "type": "ipv4",
        "latitude": 28.48533058166504,
        "longitude": -81.46553802490234,
        "region_code": "FL",
        "region_name": "FL",
        "country_code": "US",
        "country_name": "United States",
        "continent_code": "NA",
        "continent_name": "North America",
    }
    return mixin


def test_ip_address_mixin(ip_address_mixin):
    ip_data = ip_address_mixin.ip_parsed()
    assert isinstance(ip_data, IPAddressData)
    assert ip_data.city == "Orlando"
    assert ip_data.region_code == "FL"
    assert ip_data.country_name == "United States"
    assert ip_address_mixin.location == "Orlando, FL (United States)"
