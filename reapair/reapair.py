#!/usr/bin/env python3

# ReapAir is a tool to generate and distribute useful repair instructions for your everyday life.
# Copyright (C) 2020  ReapAir developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import click
import datetime
import random
import sys

from .helpers import get_sentences, get_template
from pathlib import Path
from .settings import DEFAULT_TEMPLATE

cwd = Path.cwd()


def generateHTML(instructions, template_path, out, overwrite=False):
    """
    Renders a HTML file ready to be printed and saves it at the given location.
    """
    try:
        template = get_template(Path(template_path))
    except Exception as e:
        sys.exit(e)

    result = template.render(instructions=instructions)

    out_path = Path(out)

    if out_path.exists() and not overwrite:
        raise FileExistsError(f"File {out} already exists and will not be overwritten.")
    with open(out_path, "w") as outfile:
        outfile.write(result)


def mixupSentences(sentences, n):
    """
    Selects a subset of sentences and returnes them in random order.
    """
    if n > len(sentences):
        n = len(sentences)

    return random.sample(sentences, n)


@click.option(
    "--lang",
    "-l",
    type=click.Choice(["de_DE"]),
    default="de_DE",
    help="Set the language of the generated repair instructions.",
)
@click.option("-n", default=10, help="Number of instructions to be created.")
@click.option(
    "--quiet",
    is_flag=True,
    default=False,
    help="Do not print the sentences to STDOUT. Default: False",
)
@click.option(
    "--html", is_flag=True, default=False, help="Render HTML output. Default: False"
)
@click.option(
    "--template",
    type=click.Path(),
    default=str(DEFAULT_TEMPLATE),
    help="Specify a custom HTML template to be used.",
)
@click.option(
    "--out",
    default=f"reapair_{datetime.datetime.now().isoformat()}.html",
    help="Filename of the HTML output file.",
)
@click.option("--overwrite", default=False, help="Overwrite existing HTML output file.")
@click.command()
def cli(lang, n, quiet, html, template, out, overwrite):
    """
    reapAir is a tool to generate and distribute useful repair instructions for your everyday life.
    """
    try:
        sentences = get_sentences(lang)
    except Exception as e:
        sys.exit(e)

    instructions = mixupSentences(sentences, n)

    if not quiet:
        for instruction in instructions:
            print(instruction)

    if html:
        try:
            generateHTML(instructions, template, out, overwrite)
        except Exception as e:
            sys.exit(e)
