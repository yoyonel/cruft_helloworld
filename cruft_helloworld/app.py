#!/usr/bin/env python -*- coding: utf-8 -*-
"""
Usage: app.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  hello-world*  Print a Hello-World message


Usage: app.py hello-world [OPTIONS]

Options:
  --globe-emoji [EUROPE_AFRICA|ASIA_AUSTRALIA|AMERICAS|WITH_MERIDIANS]
  --help                          Show this message and exit.
"""
from typing import Optional

import click
from click_default_group import DefaultGroup
from rich.console import Console

from cruft_helloworld.tools.enums import GlobeEmoji
from cruft_helloworld.tools.globe_emoji_with_geoip import (
    find_globe_emoji_from_external_ip,
)

console = Console()


# https://pypi.org/project/click-default-group/
@click.group(cls=DefaultGroup, default="hello-world", default_if_no_args=True)
def cli():
    pass


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


if __name__ == '__main__':
    cli()
