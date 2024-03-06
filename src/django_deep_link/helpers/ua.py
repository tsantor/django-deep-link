def get_ua_platform(user_agent):
    """Get platform (mobile, tablet, pc)."""
    if user_agent.is_mobile:
        return "mobile"
    elif user_agent.is_tablet:
        return "tablet"
    elif user_agent.is_pc:
        return "pc"
    else:
        return "unknown"


def get_platform_bools(user_agent):
    """Return if we're on a pc, mobile or tablet platform."""

    is_pc_mac = False
    is_pc_windows = False
    is_mobile_ios = False
    is_mobile_android = False
    is_tablet_ios = False
    is_tablet_android = False

    if user_agent.is_mobile:
        if user_agent.os.family == "iOS":
            is_mobile_ios = True
        elif user_agent.os.family == "Android":
            is_mobile_android = True

    elif user_agent.is_tablet:
        if user_agent.os.family == "iOS":
            is_tablet_ios = True
        elif user_agent.os.family == "Android":
            is_tablet_android = True

    elif user_agent.is_pc:
        if user_agent.os.family == "Mac OS X":
            is_pc_mac = True
        elif user_agent.os.family == "Windows":
            is_pc_windows = True

    return {
        "is_pc_mac": is_pc_mac,
        "is_pc_windows": is_pc_windows,
        "is_mobile_ios": is_mobile_ios,
        "is_mobile_android": is_mobile_android,
        "is_tablet_ios": is_tablet_ios,
        "is_tablet_android": is_tablet_android,
    }


def ua_to_dict(user_agent):
    """Return User Agent data as a dict."""
    return {
        "browser": dict(user_agent.browser._asdict()),
        "os": dict(user_agent.os._asdict()),
        "device": dict(user_agent.device._asdict()),
        "platform": get_ua_platform(user_agent),
    }
