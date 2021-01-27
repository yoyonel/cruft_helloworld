#!/usr/bin/env python -*- coding: utf-8 -*-
"""
Usage: app.py [OPTIONS] COMMAND [ARGS]...

Options:
  --log-level [CRITICAL|FATAL|ERROR|WARN|WARNING|INFO|DEBUG|NOTSET]
                                  set logging level
  --help                          Show this message and exit.

Commands:
  hello-world*  Print a Hello-World message

---

Usage: app.py hello-world [OPTIONS]

Options:
  --globe-emoji [EUROPE_AFRICA|ASIA_AUSTRALIA|AMERICAS|WITH_MERIDIANS]
  --help                          Show this message and exit.
"""
import logging
from typing import Optional

import click
import pyfiglet
from click_default_group import DefaultGroup
from rich.console import Console

from cruft_helloworld import __version__
from cruft_helloworld.services.globe_emoji_with_geoip import (
    find_globe_emoji_from_external_ip,
)
from cruft_helloworld.tools.config_loggers import config_loggers
from cruft_helloworld.tools.enums import GlobeEmoji

console = Console()

logger = logging.getLogger(__name__)


PACKAGE_NAME = "cruft_helloworld"
PACKAGE_VERSION = __version__


# https://pypi.org/project/click-default-group/
# TODO: find a way to define log-level without removing default group command
@click.option(
    "--log-level",
    type=click.Choice(logging._nameToLevel.keys()),
    default="WARN",
    show_default=True,
    help="set logging level",
)
@click.option(
    "-v",
    "--verbose",
    # https://click.palletsprojects.com/en/7.x/options/#counting
    count=True,
)
@click.version_option(prog_name="cruft_helloworld")
@click.option("--show-banner", is_flag=True, help="Show a ASCII banner")
@click.group(
    cls=DefaultGroup,
    default="hello-world",
    default_if_no_args=True,
    invoke_without_command=True,
)
def cli(log_level, verbose, show_banner):
    if verbose:
        default_logger_level = "INFO" if verbose == 1 else "DEBUG"
    else:
        default_logger_level = getattr(logging, log_level.upper())
    config_loggers(default_logger_level=default_logger_level)
    if show_banner:
        # print the ASCII banner
        pyfiglet.print_figlet(f"{PACKAGE_NAME}, version {PACKAGE_VERSION}")


@cli.command(short_help="Print a Hello-World message")
@click.option(
    "--globe-emoji",
    required=False,
    default=None,
    # https://github.com/pallets/click/issues/605#issuecomment-667726724
    type=click.Choice(
        [e_global_emoji.name for e_global_emoji in GlobeEmoji], case_sensitive=False
    ),
    callback=lambda ctx, param, value: getattr(GlobeEmoji, value).value
    if value
    else None,
)
def hello_world(globe_emoji: Optional[str]):
    globe_emoji = globe_emoji or find_globe_emoji_from_external_ip()
    console.print(f"Hello :{globe_emoji}:")


# https://www.python.org/dev/peps/pep-0484/
cli.set_default_command(hello_world)  # type: ignore

if __name__ == "__main__":
    cli()
