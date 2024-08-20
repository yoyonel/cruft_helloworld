from contextlib import ExitStack as DoesNotRaise
from dataclasses import dataclass, field
from ipaddress import IPv4Address
from typing import Any, ContextManager, Optional

import pytest
from parametrization import Parametrization

from cruft_helloworld.services.globe_emoji_with_geoip import (
    find_globe_emoji_from_external_ip,
    get_external_ipv4,
)
from cruft_helloworld.tools.enums import GlobeEmoji
from tests.tools.default_parameter import get_default_parameter
from tests.tools.monkeypath_target import build_target

# https://docs.pytest.org/en/latest/example/parametrize.html#parametrizing-conditional-raising
from tests.tools.parametrization_case import IParametrizationCase

nullcontext_instance = DoesNotRaise()


@dataclass
class ParametrizationCase(IParametrizationCase):
    external_ip: Optional[str]
    e_globe_emoji_expected: GlobeEmoji
    raises_context_expected: ContextManager[Any] = field(default=nullcontext_instance)

    def __post_init__(self, *args, **kwargs) -> None:
        """
        Perform a dynamic validation (after instancing)
        """
        super().__post_init__(*args, **kwargs)

        # if external_ip is defined
        if self.external_ip:
            try:
                # validate with ipaddress.IPv4Address
                IPv4Address(self.external_ip)
            except ValueError:
                raise ValueError(f"{self.external_ip=} is not a valid IPV4 address")  # type: ignore


# https://github.com/singular-labs/parametrization
@Parametrization.autodetect_parameters()
@ParametrizationCase.case(
    # create parametrize case without pytest name (and without validation)
    # ParametrizationCase.create(
    #     external_ip="57.82.224.0", e_globe_emoji_expected=GlobeEmoji.EUROPE_AFRICA
    # )
    ParametrizationCase("", "57.82.224.0", GlobeEmoji.EUROPE_AFRICA)
)
@ParametrizationCase.case(
    ParametrizationCase("IP from Chile", "8.242.200.0", GlobeEmoji.AMERICAS)
)
@ParametrizationCase.case(
    ParametrizationCase("IP from Japan", "1.72.0.0", GlobeEmoji.ASIA_AUSTRALIA)
)
@ParametrizationCase.case(
    ParametrizationCase("IP from Australia", "1.120.0.0", GlobeEmoji.ASIA_AUSTRALIA)
)
@ParametrizationCase.case(
    ParametrizationCase(
        # "Can't find external ip", None, lazy_fixture("default_iso_code_continent_emoji")
        "Can't find external ip",
        None,
        get_default_parameter(
            find_globe_emoji_from_external_ip, "default_iso_code_continent_emoji"
        ),
    )
)
@ParametrizationCase.case(
    ParametrizationCase(
        "[FAIL] Indonesia -> America",
        "23.212.112.0",
        GlobeEmoji.ASIA_AUSTRALIA,
        pytest.raises(AssertionError),
    )
)
@pytest.mark.use_internet
def test_find_globe_emoji_with_world_ips(
    monkeypatch,
    # ParametrizationCase fields
    external_ip,
    e_globe_emoji_expected,
    raises_context_expected,
):
    # https://docs.pytest.org/en/stable/reference.html?highlight=setatt#pytest.MonkeyPatch.setattr
    monkeypatch.setattr(build_target(get_external_ipv4), lambda: external_ip)
    with raises_context_expected:
        assert find_globe_emoji_from_external_ip() == e_globe_emoji_expected.value


@pytest.mark.use_internet
def test_get_external_ipv4():
    """
    Basic test for validate the external ip address retrieve (from DuckDuckGo JSON API)
    => 4 digits separate by '.'
    """
    external_ipv4 = get_external_ipv4()
    assert external_ipv4
    assert len(list(map(int, format(external_ipv4).split(".")))) == 4


@pytest.mark.use_internet
def test_find_globe_emoji_from_external_ip():
    """
    Basic test on finding a valid emoji from external ip
    """
    assert find_globe_emoji_from_external_ip() in [ge.value for ge in GlobeEmoji]
