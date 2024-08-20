import logging

import pytest
import requests

from cruft_helloworld import __project_name__
from cruft_helloworld.services.globe_emoji_with_geoip import (
    URI_TO_DDG_API,
    find_globe_emoji_from_external_ip,
    get_external_ipv4,
)
from tests.tools.default_parameter import get_default_parameter


@pytest.mark.parametrize(
    "side_effect,error_log_msg",
    (
        # Simulate no internet available
        (
            requests.exceptions.RequestException,
            f"Can't perform internet request: requests.get({URI_TO_DDG_API})!",
        ),
        # Simulate HTTP request timeout for getting external ip(v4)
        (
            requests.exceptions.Timeout,
            f"Timeout (={get_default_parameter(get_external_ipv4, 'default_timeout'):.5f}) occurred on "
            f"request: requests.get({URI_TO_DDG_API})!",
        ),
    ),
)
def test_find_globe_emoji_with_errors(
    mocker,
    caplog,
    default_iso_code_continent_emoji,
    side_effect,
    error_log_msg,
):
    mocker.patch(
        "cruft_helloworld.services.globe_emoji_with_geoip.requests.get",
        side_effect=side_effect,
    )

    with caplog.at_level(logging.DEBUG):
        result_emoji = find_globe_emoji_from_external_ip()
        expected_emoji = default_iso_code_continent_emoji.value
        assert result_emoji == expected_emoji

    records = [record for record in caplog.records if __project_name__ in record.name]
    assert len(records) == 2, records
    assert records[0].levelname == "ERROR"
    # error_msg = f"Can't perform internet request: requests.get({URI_TO_DDG_API})!"
    assert records[0].message == error_log_msg
    assert records[1].levelname == "DEBUG"
    assert records[1].message == "No external IP found"
