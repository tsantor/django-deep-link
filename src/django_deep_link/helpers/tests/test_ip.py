from ..ip import is_private_ip


def test_is_private_ip():
    # private ipv4
    assert is_private_ip("192.168.0.1") is True
    assert is_private_ip("10.0.0.1") is True
    assert is_private_ip("172.16.0.1") is True
    assert is_private_ip("127.0.0.1") is True

    # public ipv4
    assert is_private_ip("8.8.8.8") is False
    # assert is_private_ip("2001:db8::") is False
    # assert is_private_ip("fd00::") is True
    assert is_private_ip("invalid") is False
