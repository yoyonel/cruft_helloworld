import re

import pytest
from rich._emoji_codes import EMOJI

from cruft_helloworld.app import cli, console, hello_world


def test_app_cli_version(cli_runner, version_option_message):
    result = cli_runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert result.output == version_option_message


def test_app_cli_banner(cli_runner, version_option_message):
    result = cli_runner.invoke(cli, ["--banner"])
    assert result.exit_code == 0
    assert len(result.output) > len(version_option_message)
    assert result.output.count("\n") > 5


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
    with console.capture() as capture:
        result = cli_runner.invoke(
            hello_world, ["--globe-emoji", input_globe_emoji_name]
        )
    assert result.exit_code == 0
    assert capture.get() == f"Hello {expected_globe_emoji_char}\n"


def test_error_app_cli_hello_world(cli_runner):
    wrong_emoji_name = "dummy_emoji"
    result = cli_runner.invoke(hello_world, ["--globe-emoji", wrong_emoji_name])
    assert result.exit_code == 2
    assert f"invalid choice: {wrong_emoji_name}." in result.output


@pytest.mark.use_internet
def test_app_cli_hello_world_without_option(cli_runner):
    with console.capture() as capture:
        result = cli_runner.invoke(hello_world)
    assert result.exit_code == 0
    hello_world_result = capture.get()
    regex = r"Hello (?P<globe_emoji>.)"
    match = re.match(regex, hello_world_result)
    assert match, f"Can't find emoji in: '{hello_world_result}'"
    assert (
        match["globe_emoji"] in EMOJI.values()
    ), f"Emoji: '{match['globe_emoji']}' not in EMOJI dict from rich.console !"
