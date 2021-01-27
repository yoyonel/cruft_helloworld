import pytest

from cruft_helloworld import PACKAGE_NAME, __version__
from cruft_helloworld.app import cli
from cruft_helloworld.services.globe_emoji_with_geoip import (
    find_globe_emoji_from_external_ip,
)
from cruft_helloworld.tools.enums import IsoCodeContinentEmoji
from tests.tools.default_parameter import get_default_parameter


@pytest.fixture(autouse=True)
def setup_log_level_to_debug(cli_runner):
    cli_runner.invoke(cli, ["--log-level", "DEBUG"])


@pytest.fixture(scope="session")
def default_iso_code_continent_emoji() -> IsoCodeContinentEmoji:
    return get_default_parameter(
        find_globe_emoji_from_external_ip, "default_iso_code_continent_emoji"
    )


@pytest.fixture(scope="session")
def version_option_message():
    return f"{PACKAGE_NAME}, version {__version__}\n"
