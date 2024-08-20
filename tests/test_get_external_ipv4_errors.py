import logging

from cruft_helloworld import __project_name__
from cruft_helloworld.services.globe_emoji_with_geoip import (
    URI_TO_DDG_API,
    get_external_ipv4,
)


def test_cant_extract_ip_address_error(requests_mock, caplog):
    mock_external_ipv4 = "Your IP address is dummy_ip in"
    mock_request_response = f'{{"Answer":  "{mock_external_ipv4}"}}'
    requests_mock.get(URI_TO_DDG_API, text=mock_request_response)

    with caplog.at_level(logging.ERROR):
        assert get_external_ipv4() is None

    records = [record for record in caplog.records if __project_name__ in record.name]
    assert len(records) == 1, records
    assert records[0].levelname == "ERROR"
    assert records[0].message == f"Can't extract ip_address from: {mock_external_ipv4}"


def test_not_valid_json_request_response_error(requests_mock, caplog):
    mock_request_response = ""
    requests_mock.get(URI_TO_DDG_API, text=mock_request_response)

    with caplog.at_level(logging.ERROR):
        assert get_external_ipv4() is None

    records = [record for record in caplog.records if __project_name__ in record.name]
    assert len(records) == 1, records
    assert records[0].levelname == "ERROR"
    expected_msg_error = (
        f"Can't perform internet request: requests.get({URI_TO_DDG_API})!"
    )
    assert records[0].message == expected_msg_error
