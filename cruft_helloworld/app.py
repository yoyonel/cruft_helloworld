#!/usr/bin/env python -*- coding: utf-8 -*-
"""
Usage: app.py hello-world [OPTIONS]

Options:
  --map_emoji [EUROPE-AFRICA|ASIA_AUSTRALIA|AMERICAS|MERIDIANS]
  -h, --help                      Show this message and exit.
"""
from typing import Dict

import click
from rich.console import Console

console = Console()

globes_emojis: Dict[str, str] = {
    "EUROPE-AFRICA": "globe_showing_europe-africa",
    "ASIA-AUSTRALIA": "globe_showing_asia-australia",
    "AMERICAS": "globe_showing_americas",
    "WITH_MERIDIANS": "globe_with_meridians",
}


@click.command(short_help="Print a Hello-World message")
@click.option(
    "--map_emoji",
    default="EUROPE-AFRICA",
    required=False,
    # https://github.com/pallets/click/issues/605#issuecomment-667726724
    type=click.Choice(list(map(lambda x: x, globes_emojis)), case_sensitive=False),
)
def hello_world(map_emoji: str):
    console.print(f"Hello :{globes_emojis[map_emoji]}:")


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def entry_point():
    pass


entry_point.add_command(hello_world)

if __name__ == "__main__":
    entry_point()
