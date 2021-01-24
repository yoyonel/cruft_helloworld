import logging
import sys
from contextlib import ExitStack as DoesNotRaise
from dataclasses import dataclass, field
from typing import Any, ContextManager, Optional

import pytest
import requests
from parametrization import Parametrization
from pytest_lazyfixture import lazy_fixture

from cruft_helloworld.services.globe_emoji_with_geoip import (
    find_globe_emoji_from_external_ip,
    get_external_ipv4,
)
from cruft_helloworld.tools.enums import GlobeEmoji
from tests.tools.monkeypath_target import build_target

# https://docs.pytest.org/en/latest/example/parametrize.html#parametrizing-conditional-raising
from tests.tools.parametrization_case import IParametrizationCase

nullcontext_instance = DoesNotRaise()


@dataclass
class ParametrizationCase(IParametrizationCase):
    external_ip: Optional[str]
    e_globe_emoji_expected: GlobeEmoji
    raises_context_expected: ContextManager[Any] = field(default=nullcontext_instance)


# https://github.com/singular-labs/parametrization
@Parametrization.autodetect_parameters()
@IParametrizationCase.case(
    # create parametrize case without pytest name
    ParametrizationCase.create(
        external_ip="57.82.224.0", e_globe_emoji_expected=GlobeEmoji.EUROPE_AFRICA
    )
)
@IParametrizationCase.case(
    ParametrizationCase("IP from Chile", "8.242.200.0", GlobeEmoji.AMERICAS)
)
@IParametrizationCase.case(
    ParametrizationCase("IP from Japan", "1.72.0.0", GlobeEmoji.ASIA_AUSTRALIA)
)
@IParametrizationCase.case(
    ParametrizationCase("IP from Australia", "1.120.0.0", GlobeEmoji.ASIA_AUSTRALIA)
)
@IParametrizationCase.case(
    ParametrizationCase(
        "Can't find external ip", None, lazy_fixture("default_iso_code_continent_emoji")
    )
)
@IParametrizationCase.case(
    ParametrizationCase(
        "[FAIL] Indonesia -> America",
        "23.212.112.0",
        GlobeEmoji.ASIA_AUSTRALIA,
        pytest.raises(AssertionError),
    )
)
def test_find_globe_emoji_with_world_ips(
    monkeypatch, external_ip, e_globe_emoji_expected, raises_context_expected
):
    # https://docs.pytest.org/en/stable/reference.html?highlight=setatt#pytest.MonkeyPatch.setattr
    monkeypatch.setattr(build_target(get_external_ipv4), lambda: external_ip)
    with raises_context_expected:
        assert find_globe_emoji_from_external_ip() == e_globe_emoji_expected.value


def test_find_globe_emoji_with_no_internet(
    caplog, monkeypatch, default_iso_code_continent_emoji
):
    def _requests_get(*_args, **_kwargs):
        raise requests.exceptions.RequestException

    monkeypatch.setattr(
        "cruft_helloworld.services.globe_emoji_with_geoip.requests.get", _requests_get
    )
    with caplog.at_level(logging.DEBUG):
        result = find_globe_emoji_from_external_ip()
    expected = default_iso_code_continent_emoji.value
    assert result == expected

    records = [record for record in caplog.records if 'cruft_helloworld' in record.name]
    assert len(records) == 2, records
    assert records[0].levelname == "ERROR"
    error_msg = "Can't perform internet request: requests.get(https://api.duckduckgo.com/?q=ip&format=json)!"
    assert records[0].message == error_msg
    assert records[1].levelname == "DEBUG"
    assert records[1].message == "No external IP found"


@pytest.mark.use_internet
def test_find_globe_emoji_with_timeout(
    caplog, monkeypatch, default_iso_code_continent_emoji
):
    # set timeout to minimal float representation in Python
    # so it's impossible (float precision/speed) to perform the request with this timeout
    # https://docs.python.org/3/library/sys.html#sys.float_info
    test_timeout = sys.float_info.min

    def _get_external_ipv4(*_args, **_kwargs):
        return get_external_ipv4(default_timeout=test_timeout)

    monkeypatch.setattr(build_target(get_external_ipv4), _get_external_ipv4)
    caplog.set_level(logging.DEBUG)

    # https://stackoverflow.com/questions/12627118/get-a-function-arguments-default-value
    assert find_globe_emoji_from_external_ip() == default_iso_code_continent_emoji.value

    records = [record for record in caplog.records if 'cruft_helloworld' in record.name]
    assert len(records) == 2, records
    assert records[0].levelname == "ERROR"
    error_msg = f"Timeout (={test_timeout:.5f}) occurred on request: requests.get(https://api.duckduckgo.com/?q=ip&format=json)!"
    assert records[0].message == error_msg
    assert records[1].levelname == "DEBUG"
    assert records[1].message == "No external IP found"


@pytest.mark.use_internet
def test_get_external_ipv4():
    """
    Basic test for validate the external ip address retrieve (from DuckDuckGo JSON API)
    => 4 digits separate by '.'
    """
    assert len(list(map(int, format(get_external_ipv4()).split(".")))) == 4


@pytest.mark.use_internet
def test_find_globe_emoji_from_external_ip():
    """
    Basic test on finding a valid emoji from external ip
    """
    assert find_globe_emoji_from_external_ip() in map(lambda ge: ge.value, GlobeEmoji)
