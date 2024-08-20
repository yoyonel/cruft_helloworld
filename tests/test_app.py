import re

import pytest
from rich._emoji_codes import EMOJI

from cruft_helloworld import __project_name__ as application_name
from cruft_helloworld import __version__ as application_version
from cruft_helloworld.app import cli, hello_world


def test_app_cli_option_version(cli_runner):
    result = cli_runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    application_name_expected = application_name
    application_version_expected = application_version
    version_message_expected = (
        f"{application_name_expected}, version {application_version_expected}\n"
    )
    assert result.output == version_message_expected


# @pytest.mark.skip
def test_app_cli_option_show_banner(cli_runner):
    result = cli_runner.invoke(cli, ["--show-banner"])
    assert result.exit_code == 0
    version_message = f"{application_name}, version {application_version}"
    assert len(result.output) > len(version_message)
    assert result.output.count("\n") > 1


def test_app_cli_option_verbose(cli_runner):
    result = cli_runner.invoke(cli, ["--verbose"])
    assert result.exit_code == 0
    assert "DEBUG" not in result.output

    result = cli_runner.invoke(cli, ["-vv"])
    assert result.exit_code == 0
    assert "DEBUG" in result.output


def test_app_cli_help(cli_runner):
    result = cli_runner.invoke(hello_world, ["--help"])
    assert result.exit_code == 0
    assert (
        "--globe-emoji [EUROPE_AFRICA|ASIA_AUSTRALIA|AMERICAS|WITH_MERIDIANS]"
        in result.output
    )


@pytest.mark.parametrize(
    "input_globe_emoji_name,expected_globe_emoji_char",
    (
        ("EUROPE_AFRICA", "🌍"),
        ("americas", "🌎"),
        ("ASiA_AUStRAliA", "🌏"),
        ("wITH_MERIDIAnS", "🌐"),
    ),
)
def test_app_cli_hello_world(
    cli_runner, input_globe_emoji_name: str, expected_globe_emoji_char: str
):
    # https://github.com/willmcgugan/rich/blob/a3f5609202e9aa45751ce9baa3a72462ed1cc488/tests/test_console.py#L192
    result = cli_runner.invoke(hello_world, ["--globe-emoji", input_globe_emoji_name])
    assert result.exit_code == 0
    assert result.output == f"Hello {expected_globe_emoji_char}\n"


def test_error_app_cli_hello_world(cli_runner):
    click_option_name = "globe-emoji"
    wrong_emoji_name = "no-existing-click-option"
    result = cli_runner.invoke(
        hello_world, [f"--{click_option_name}", wrong_emoji_name]
    )
    assert result.exit_code == 2
    assert (
        f"Error: Invalid value for '--{click_option_name}': '{wrong_emoji_name}'"
        in result.output
    )


@pytest.mark.use_internet
def test_app_cli_hello_world_without_option(cli_runner):
    result = cli_runner.invoke(hello_world)
    assert result.exit_code == 0
    hello_world_result = result.output
    regex = r"Hello (?P<globe_emoji>.)"
    match = re.match(regex, hello_world_result)
    assert match, f"Can't find emoji in: '{hello_world_result}'"
    assert (
        match["globe_emoji"] in EMOJI.values()
    ), f"Emoji: '{match['globe_emoji']}' not in EMOJI dict from rich.console !"
