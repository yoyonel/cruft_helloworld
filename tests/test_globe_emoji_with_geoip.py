import pytest

from cruft_helloworld.tools.enums import GlobeEmoji
from cruft_helloworld.tools.globe_emoji_with_geoip import (
    find_globe_emoji_from_external_ip,
    get_external_ip,
)

pytestmark = pytest.mark.external


def test_get_external_ip():
    """
    Basic test for validate the external ip address retrieve (from duckduck JSON API)
    => 4 digits separate by '.'
    """
    assert len(list(map(int, get_external_ip().split(".")))) == 4


def test_get_external_ip_with_fail(mocker):
    # TODO: mock on 'requests.get(...)' and test with none result
    pass


def test_find_globe_emoji_from_external_ip():
    """
    Basic test on finding a valid emoji from external ip
    """
    assert find_globe_emoji_from_external_ip() in [enum.value for enum in GlobeEmoji]


@pytest.mark.parametrize(
    "external_ip,e_globe_emoji_expected",
    (
        ("57.82.224.0", GlobeEmoji.EUROPE_AFRICA),  # Congo
        ("8.242.200.0", GlobeEmoji.AMERICAS),  # Chile
        # ("23.212.112.0", GlobeEmoji.ASIA_AUSTRALIA),    # Indonesia (Fail -> america)
        ("1.72.0.0", GlobeEmoji.ASIA_AUSTRALIA),  # Japan
        ("1.120.0.0", GlobeEmoji.ASIA_AUSTRALIA),  # Australia
    ),
)
def test_find_globe_emoji_with_mock(mocker, external_ip, e_globe_emoji_expected):
    def _get_external_ip() -> str:
        return external_ip

    # TODO: update pytest-mock version and change (accordingly with) the (new) mock strategy
    with mocker.patch(
        "cruft_helloworld.tools.globe_emoji_with_geoip.get_external_ip",
        side_effect=_get_external_ip,
    ):
        assert find_globe_emoji_from_external_ip() == e_globe_emoji_expected.value
