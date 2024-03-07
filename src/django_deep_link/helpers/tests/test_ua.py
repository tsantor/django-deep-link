import pytest
from django.test import RequestFactory
from user_agents import parse

from ..ua import get_platform_bools, get_ua, get_ua_info, get_ua_platform


@pytest.mark.parametrize(
    "user_agent,expected_platform",
    [
        (
            "Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3",  # noqa
            "mobile",
        ),
        (
            "Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53",  # noqa
            "tablet",
        ),
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",  # noqa
            "pc",
        ),
        (
            "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "unknown",
        ),
    ],
)
def test_get_ua_platform(user_agent, expected_platform):
    ua = parse(user_agent)
    assert get_ua_platform(ua) == expected_platform


@pytest.mark.parametrize(
    "user_agent",
    [
        "Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3",  # noqa
        "Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53",  # noqa
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",  # noqa
        "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    ],
)
def test_get_ua(user_agent):
    factory = RequestFactory(headers={"user-agent": user_agent})
    request = factory.get("/")
    assert get_ua(request) == user_agent


@pytest.mark.parametrize(
    "user_agent",
    [
        "Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3",  # noqa
        "Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53",  # noqa
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",  # noqa
        "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    ],
)
def test_get_ua_info(user_agent):
    ua_info = get_ua_info(user_agent)

    assert isinstance(ua_info, dict)
    assert "browser" in ua_info
    assert "os" in ua_info
    assert "device" in ua_info
    assert "platform" in ua_info

    assert isinstance(ua_info["browser"], dict)
    assert isinstance(ua_info["os"], dict)
    assert isinstance(ua_info["device"], dict)
    assert isinstance(ua_info["platform"], str)
    assert isinstance(ua_info["platform"], str)
    assert isinstance(ua_info["platform"], str)


@pytest.mark.parametrize(
    "user_agent,expected_result",
    [
        (
            "Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3",  # noqa
            {
                "is_pc_mac": False,
                "is_pc_windows": False,
                "is_mobile_ios": True,
                "is_mobile_android": False,
                "is_tablet_ios": False,
                "is_tablet_android": False,
            },
        ),
        (
            "Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53",  # noqa
            {
                "is_pc_mac": False,
                "is_pc_windows": False,
                "is_mobile_ios": False,
                "is_mobile_android": False,
                "is_tablet_ios": True,
                "is_tablet_android": False,
            },
        ),
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",  # noqa
            {
                "is_pc_mac": False,
                "is_pc_windows": True,
                "is_mobile_ios": False,
                "is_mobile_android": False,
                "is_tablet_ios": False,
                "is_tablet_android": False,
            },
        ),
        (
            "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            {
                "is_pc_mac": False,
                "is_pc_windows": False,
                "is_mobile_ios": False,
                "is_mobile_android": False,
                "is_tablet_ios": False,
                "is_tablet_android": False,
            },
        ),
    ],
)
def test_get_platform_bools(user_agent, expected_result):
    ua = parse(user_agent)
    assert get_platform_bools(ua) == expected_result
