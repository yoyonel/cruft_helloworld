#!/usr/bin/env python -*- coding: utf-8 -*-
"""
Usage: app.py hello-world [OPTIONS]

Options:
  --globe-emoji [EUROPE_AFRICA|ASIA_AUSTRALIA|AMERICAS|WITH_MERIDIANS]
  -h, --help                      Show this message and exit.
"""
from enum import Enum

import click
from rich.console import Console

console = Console()


class GlobeEmoji(Enum):
    """
    Declare enums for click option (`--globe-emoji`)
    and do (in the same time) a mapping between enum -> emoji name
    """

    EUROPE_AFRICA = "globe_showing_europe-africa"
    ASIA_AUSTRALIA = "globe_showing_asia-australia"
    AMERICAS = "globe_showing_americas"
    WITH_MERIDIANS = "globe_with_meridians"


@click.command(short_help="Print a Hello-World message")
@click.option(
    "--globe-emoji",
    default="EUROPE_AFRICA",
    required=False,
    # https://github.com/pallets/click/issues/605#issuecomment-667726724
    type=click.Choice(
        [e_global_emoji.name for e_global_emoji in GlobeEmoji], case_sensitive=False
    ),
    callback=lambda ctx, param, value: getattr(GlobeEmoji, value).value
    if value
    else None,
)
def hello_world(globe_emoji: str):
    console.print(f"Hello :{globe_emoji}:")


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def entry_point():
    pass


entry_point.add_command(hello_world)

if __name__ == "__main__":
    entry_point()
