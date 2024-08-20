import pytest

from cruft_helloworld.services.globe_emoji_with_geoip import (
    find_globe_emoji_from_external_ip,
)
from cruft_helloworld.tools.enums import IsoCodeContinentEmoji
from tests.tools.default_parameter import get_default_parameter


@pytest.fixture(scope="session")
def default_iso_code_continent_emoji() -> IsoCodeContinentEmoji:
    return get_default_parameter(
        find_globe_emoji_from_external_ip, "default_iso_code_continent_emoji"
    )
