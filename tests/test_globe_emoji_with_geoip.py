import pytest

from cruft_helloworld.tools.enums import GlobeEmoji
from cruft_helloworld.tools.globe_emoji_with_geoip import (
    find_globe_emoji_from_external_ip,
    get_external_ip,
)


@pytest.mark.external
def test_get_external_ip():
    assert len(list(map(int, get_external_ip().split(".")))) == 4


def test_get_external_ip_with_fail(mocker):
    # TODO: mock on 'requests.get(...)' and test with none result
    pass


@pytest.mark.external
def test_find_globe_emoji_from_external_ip():
    assert find_globe_emoji_from_external_ip() in [enum.value for enum in GlobeEmoji]
