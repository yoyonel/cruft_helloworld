#!/usr/bin/env python -*- coding: utf-8 -*-
"""
Usage: app.py [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  hello-world  Print a Hello-World message


Usage: app.py hello-world [OPTIONS]

Options:
  --globe-emoji [EUROPE_AFRICA|ASIA_AUSTRALIA|AMERICAS|WITH_MERIDIANS]
  -h, --help                      Show this message and exit.
"""
from typing import Optional

import click
from rich.console import Console

from cruft_helloworld.tools.enums import GlobeEmoji
from cruft_helloworld.tools.globe_emoji_with_geoip import (
    find_globe_emoji_from_external_ip,
)

console = Console()


@click.command(short_help="Print a Hello-World message")
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


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def entry_point():
    pass


entry_point.add_command(hello_world)

if __name__ == "__main__":
    entry_point()
