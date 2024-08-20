import logging
import re
from ipaddress import IPv4Address, IPv6Address, ip_address
from typing import Final, Optional, Union

import requests
from geoip import IPInfo, geolite2

from cruft_helloworld import __project_name__
from cruft_helloworld.tools.enums import IsoCodeContinentEmoji

URI_TO_DDG_API: Final[str] = "https://api.duckduckgo.com/?q=ip&format=json"

logger = logging.getLogger(__project_name__)


def get_external_ipv4(
    default_timeout: float = 1.0,
) -> Optional[Union[IPv4Address, IPv6Address]]:
    """
    Use DuckDuckGo (external communication) for resolve external ip
    """
    # https://api.duckduckgo.com/api
    external_ip = None
    try:
        # https://requests.readthedocs.io/en/master/user/quickstart/#timeouts
        raw = requests.get(URI_TO_DDG_API, timeout=default_timeout)
        answer: str = raw.json().get("Answer", "")
        logger.debug("request(%s).Answer -> %s", URI_TO_DDG_API, answer)
        # https://regex101.com/r/NMdWXw/1
        regex = (
            r"Your IP address is (?P<ip_address>[0-9]*\.[0-9]+\.[0-9]+\.[0-9]+) in.*"
        )
        match = re.match(regex, answer)
        if match is None:
            logger.error(f"Can't extract ip_address from: {answer}")
        else:
            # https://docs.python.org/3/library/ipaddress.html#ipaddress.ip_address
            external_ip = ip_address(match["ip_address"])
    except requests.exceptions.Timeout:
        logger.error(
            "Timeout (=%.5f) occurred on request: requests.get(%s)!",
            default_timeout,
            URI_TO_DDG_API,
        )
    except requests.exceptions.RequestException:
        logger.error(
            "Can't perform internet request: requests.get(%s)!", URI_TO_DDG_API
        )
    return external_ip


def find_globe_emoji_from_external_ip(
    default_iso_code_continent_emoji: IsoCodeContinentEmoji = IsoCodeContinentEmoji.EU,
) -> str:
    """
    Use external ip for finding appropriate globe emoji
    """
    external_ip = get_external_ipv4()
    if external_ip is None:
        logger.debug("No external IP found")
        return default_iso_code_continent_emoji.value

    match: Optional[IPInfo] = geolite2.lookup(format(external_ip))
    if match is None:
        logger.debug(
            "Can't provides information about the located IP = %s", external_ip
        )
        return default_iso_code_continent_emoji.value

    logger.debug("Match result from geolite = %s", match)

    try:
        iso_code_continent_emoji = IsoCodeContinentEmoji[match.continent].value
    except KeyError:
        logger.error(
            "'%s' is not a valid ISO Code continent emoji"
            " - Hint: Need to update `tools.enums.IsoCodeContinentEmoji`",
            match.continent,
        )
        iso_code_continent_emoji = default_iso_code_continent_emoji.value

    return iso_code_continent_emoji
