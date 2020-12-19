from enum import Enum


class IsoCodeContinentEmoji(Enum):
    """
    https://doc.bccnsoft.com/docs/php-docs-7-en/function.geoip-continent-code-by-name.html
    """

    AF = "globe_showing_europe-africa"  # Africa
    AN = "globe_with_meridians"  # Antarctica
    AS = "globe_showing_asia-australia"  # Asia
    EU = "globe_showing_europe-africa"  # Europe
    NA = "globe_showing_americas"  # North America
    OC = "globe_showing_asia-australia"  # Oceania
    SA = "globe_showing_americas"  # South America


class GlobeEmoji(Enum):
    """
    Declare enums for click option (`--globe-emoji`)
    and do (in the same time) a mapping between enum -> emoji name
    """

    EUROPE_AFRICA = "globe_showing_europe-africa"
    ASIA_AUSTRALIA = "globe_showing_asia-australia"
    AMERICAS = "globe_showing_americas"
    WITH_MERIDIANS = "globe_with_meridians"
