#!/usr/bin/env python3
import argparse
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

    if out_path.exists():
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
@click.option("-n", default=10, help="Set the language of the generated repair")
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
    sentences = get_sentences(lang)
    instructions = mixupSentences(sentences, n)

    if not quiet:
        for instruction in instructions:
            print(instruction)

    if html:
        generateHTML(instructions, template, out)
