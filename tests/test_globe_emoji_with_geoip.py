from contextlib import nullcontext
from typing import Any, ContextManager, Optional

import pytest
from parametrization import Parametrization

from cruft_helloworld.services.globe_emoji_with_geoip import (
    find_globe_emoji_from_external_ip,
    get_external_ip,
)
from cruft_helloworld.tools.enums import GlobeEmoji
from tests.tools.monkeypath_target import build_target

pytestmark = pytest.mark.using_geoip


def test_get_external_ip():
    """
    Basic test for validate the external ip address retrieve (from DuckDuckGo JSON API)
    => 4 digits separate by '.'
    """
    assert len(list(map(int, get_external_ip().split(".")))) == 4


def test_find_globe_emoji_from_external_ip():
    """
    Basic test on finding a valid emoji from external ip
    """
    assert find_globe_emoji_from_external_ip() in [enum.value for enum in GlobeEmoji]


def _pc(
    n: str, ei: Optional[str], egee: GlobeEmoji, rc: ContextManager[Any] = nullcontext()
) -> dict:
    return dict(name=n, external_ip=ei, e_globe_emoji_expected=egee, raises_context=rc)


# https://github.com/singular-labs/parametrization
@Parametrization.autodetect_parameters()
@Parametrization.case(**_pc("IP from Congo", "57.82.224.0", GlobeEmoji.EUROPE_AFRICA))
@Parametrization.case(**_pc("IP from Chile", "8.242.200.0", GlobeEmoji.AMERICAS))
@Parametrization.case(**_pc("IP from Japan", "1.72.0.0", GlobeEmoji.ASIA_AUSTRALIA))
@Parametrization.case(
    **_pc("IP from Australia", "1.120.0.0", GlobeEmoji.ASIA_AUSTRALIA)
)
@Parametrization.case(**_pc("Can't find external ip", None, GlobeEmoji.EUROPE_AFRICA))
@Parametrization.case(
    **_pc(
        "[FAIL] Indonesia -> America",
        "23.212.112.0",
        GlobeEmoji.ASIA_AUSTRALIA,
        rc=pytest.raises(AssertionError),
    )
)
def test_find_globe_emoji_with_mock(
    monkeypatch, external_ip, e_globe_emoji_expected, raises_context
):
    # https://docs.pytest.org/en/stable/reference.html?highlight=setatt#pytest.MonkeyPatch.setattr
    # "cruft_helloworld.tools.globe_emoji_with_geoip.get_external_ip"
    monkeypatch.setattr(build_target(get_external_ip), lambda: external_ip)
    with raises_context:
        assert find_globe_emoji_from_external_ip() == e_globe_emoji_expected.value
