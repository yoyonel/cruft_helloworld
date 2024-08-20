import logging

import pytest
import requests
from geoip import IPInfo

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
    assert records[0].message == error_log_msg
    assert records[1].levelname == "DEBUG"
    assert records[1].message == "No external IP found"


def test_geolite2_lookup_return_no_match_error(
    requests_mock,
    mocker,
    caplog,
    default_iso_code_continent_emoji,
):
    mock_external_ipv4 = "0.0.0.0"
    mock_request_answer = f"Your IP address is {mock_external_ipv4} in"
    mock_request_response = f'{{"Answer":  "{mock_request_answer}"}}'
    requests_mock.get(URI_TO_DDG_API, text=mock_request_response)

    mocker.patch(
        "cruft_helloworld.services.globe_emoji_with_geoip.geolite2.lookup",
        return_value=None,
    )

    with caplog.at_level(logging.DEBUG):
        result_emoji = find_globe_emoji_from_external_ip()
        expected_emoji = default_iso_code_continent_emoji.value
        assert result_emoji == expected_emoji

    records = [record for record in caplog.records if __project_name__ in record.name]
    assert len(records) == 2, records
    assert records[0].levelname == "DEBUG"
    expected_debug_msg = f"request({URI_TO_DDG_API}).Answer -> {mock_request_answer}"
    assert records[0].message == expected_debug_msg
    assert records[1].levelname == "DEBUG"
    expected_debug_msg = (
        f"Can't provides information about the located IP = {mock_external_ipv4}"
    )
    assert records[1].message == expected_debug_msg


def test_geolite2_lookup_return_an_unknown_match_continent_error(
    requests_mock,
    mocker,
    caplog,
    default_iso_code_continent_emoji,
):
    mock_external_ipv4 = "0.0.0.0"
    mock_request_answer = f"Your IP address is {mock_external_ipv4} in"
    mock_request_response = f'{{"Answer":  "{mock_request_answer}"}}'
    requests_mock.get(URI_TO_DDG_API, text=mock_request_response)

    unknown_code_continent = "UK"
    mock_ipinfo = IPInfo(
        ip=mock_external_ipv4, data={"continent": {"code": unknown_code_continent}}
    )
    mocker.patch(
        "cruft_helloworld.services.globe_emoji_with_geoip.geolite2.lookup",
        return_value=mock_ipinfo,
    )

    with caplog.at_level(logging.DEBUG):
        result_emoji = find_globe_emoji_from_external_ip()
        expected_emoji = default_iso_code_continent_emoji.value
        assert result_emoji == expected_emoji

    records = [record for record in caplog.records if __project_name__ in record.name]
    assert len(records) == 3, records
    assert records[0].levelname == "DEBUG"
    expected_debug_msg = f"request({URI_TO_DDG_API}).Answer -> {mock_request_answer}"
    assert records[0].message == expected_debug_msg
    assert records[1].levelname == "DEBUG"
    assert records[1].message == f"Match result from geolite = {mock_ipinfo}"
    assert records[2].levelname == "ERROR"
    assert records[2].message == (
        f"'{unknown_code_continent}' is not a valid ISO Code continent emoji "
        f"- Hint: Need to update `tools.enums.IsoCodeContinentEmoji`"
    )
