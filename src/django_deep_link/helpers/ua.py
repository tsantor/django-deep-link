from user_agents import parse
from user_agents.parsers import UserAgent

# def get_ua_platform(user_agent) -> str:
#     """Get platform (mobile, tablet, pc)."""
#     if user_agent.is_mobile:
#         return "mobile"
#     elif user_agent.is_tablet:
#         return "tablet"
#     elif user_agent.is_pc:
#         return "pc"
#     else:
#         return "unknown"


def get_ua_platform(user_agent: UserAgent) -> str:
    """Get platform (mobile, tablet, pc)."""
    platforms = {
        "mobile": user_agent.is_mobile,
        "tablet": user_agent.is_tablet,
        "pc": user_agent.is_pc,
    }
    return next(
        (platform for platform, check in platforms.items() if check),
        "unknown",
    )


def get_ua(request) -> str:
    return request.headers.get("user-agent", "")


def get_ua_info(ua_string: str) -> dict:
    """Return User Agent data as a dict."""
    user_agent = parse(ua_string)
    return {
        "browser": dict(user_agent.browser._asdict()),
        "os": dict(user_agent.os._asdict()),
        "device": dict(user_agent.device._asdict()),
        "platform": get_ua_platform(user_agent),
    }


def get_platform_bools(user_agent: UserAgent) -> dict:
    """Return if we're on a pc, mobile or tablet platform."""

    return {
        "is_pc_mac": user_agent.is_pc and user_agent.os.family == "Mac OS X",
        "is_pc_windows": user_agent.is_pc and user_agent.os.family == "Windows",
        "is_mobile_ios": user_agent.is_mobile and user_agent.os.family == "iOS",
        "is_mobile_android": user_agent.is_mobile and user_agent.os.family == "Android",
        "is_tablet_ios": user_agent.is_tablet and user_agent.os.family == "iOS",
        "is_tablet_android": user_agent.is_tablet and user_agent.os.family == "Android",
    }
