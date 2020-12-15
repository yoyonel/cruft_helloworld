import pytest

from cruft_helloworld.app import GlobeEmoji, console, hello_world


def test_app_cli_help(cli_runner):
    result = cli_runner.invoke(hello_world, ["--help"])
    assert result.exit_code == 0
    assert (
        "--globe-emoji [EUROPE_AFRICA|ASIA_AUSTRALIA|AMERICAS|WITH_MERIDIANS]"
        in result.output
    )


@pytest.mark.parametrize(
    "globe_emoji_name,globe_emoji_char",
    (
        ("", "🌍"),
        ("EUROPE_AFRICA", "🌍"),
        ("americas", "🌎"),
        ("ASiA_AUStRAliA", "🌏"),
        ("wITH_MERIDIAnS", "🌐"),
    ),
)
def test_app_cli_hello_world(
    cli_runner, globe_emoji_name: GlobeEmoji, globe_emoji_char: str
):
    # https://github.com/willmcgugan/rich/blob/a3f5609202e9aa45751ce9baa3a72462ed1cc488/tests/test_console.py#L192
    with console.capture() as capture:
        result = cli_runner.invoke(
            hello_world, ["--globe-emoji", globe_emoji_name] if globe_emoji_name else []
        )
    assert result.exit_code == 0
    assert capture.get() == f"Hello {globe_emoji_char}\n"


def test_error_app_cli_hello_world(cli_runner):
    wrong_emoji_name = "dummy_emoji"
    result = cli_runner.invoke(hello_world, ["--globe-emoji", wrong_emoji_name])
    assert result.exit_code == 2
    assert f"invalid choice: {wrong_emoji_name}." in result.output
