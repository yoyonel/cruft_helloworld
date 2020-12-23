import logging
import re
from typing import Optional

import requests
from geoip import IPInfo, geolite2

from cruft_helloworld.tools.enums import IsoCodeContinentEmoji

logger = logging.getLogger(__name__)


def get_external_ip() -> Optional[str]:
    """
    Use DuckDuckGo (external communication) for resolve external ip
    """
    # https://api.duckduckgo.com/api
    uri_to_geoip_db = "https://api.duckduckgo.com/?q=ip&format=json"
    raw = requests.get(uri_to_geoip_db)
    answer: str = raw.json().get("Answer", "")
    logger.debug("request(%s).Answer -> %s", uri_to_geoip_db, answer)
    # https://regex101.com/r/NMdWXw/1
    regex = r"Your IP address is (?P<ip_address>[0-9]*\.[0-9]+\.[0-9]+\.[0-9]+) in.*"
    match = re.match(regex, answer)
    return match["ip_address"] if match else None


def find_globe_emoji_from_external_ip(
    default_globe_emoji: str = IsoCodeContinentEmoji.EU.value,
) -> str:
    """
    Use external ip for finding appropriate globe emoji
    """
    external_ip = get_external_ip()
    if external_ip is None:
        logger.debug("No external IP found")
        return default_globe_emoji
    match: IPInfo = geolite2.lookup(external_ip)
    return IsoCodeContinentEmoji[match.continent].value
