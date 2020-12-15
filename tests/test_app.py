import pytest

from cruft_helloworld.app import console, hello_world


def test_app_cli_help(cli_runner):
    result = cli_runner.invoke(hello_world, ["--help"])
    assert result.exit_code == 0


@pytest.mark.parametrize(
    "glob_emoji_name,glob_emoji",
    (
        ("", "🌍"),
        ("EUROPE-AFRICA", "🌍"),
        ("AMERICAS", "🌎"),
        ("ASIA-AUSTRALIA", "🌏"),
        ("WITH_MERIDIANS", "🌐"),
    ),
)
def test_app_cli_hello_world(cli_runner, glob_emoji_name, glob_emoji):
    # https://github.com/willmcgugan/rich/blob/a3f5609202e9aa45751ce9baa3a72462ed1cc488/tests/test_console.py#L192
    with console.capture() as capture:
        result = cli_runner.invoke(
            hello_world, ["--map_emoji", glob_emoji_name] if glob_emoji_name else []
        )
    assert result.exit_code == 0
    assert capture.get() == f"Hello {glob_emoji}\n"


def test_error_app_cli_hello_world(cli_runner):
    wrong_emoji_name = "dummy_emoji"
    result = cli_runner.invoke(hello_world, ["--map_emoji", wrong_emoji_name])
    assert result.exit_code == 2
    assert f"invalid choice: {wrong_emoji_name}." in result.output
