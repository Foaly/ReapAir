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
import math

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


def generate_instructions(sentences_dict: dict, n):
    """
    Selects a mix of sentences according to a predefined distribution
    from the different lists contained in the dict.
    """
    if not isinstance(sentences_dict, dict):
        raise TypeError(f"'sentence_dict' must be of type 'dict', instead got '{type(sentences_dict)}'")

    safety_notes = sentences_dict["safety_notes"]
    instructions = sentences_dict["instructions"]
    conditionals = sentences_dict["conditionals"]
    finals = sentences_dict["finals"]

    if n <= 3:
        n = min(n, len(instructions))
        return random.sample(instructions, n)

    # sentence type distribution
    safety_notes_count = min(math.ceil(n * 0.2), len(safety_notes))
    conditionals_count = min(math.ceil(n * 0.1), len(conditionals))
    finals_count = 1
    instructions_count = n - (safety_notes_count + conditionals_count + finals_count)
    instructions_count = min(instructions_count, len(instructions))

    result = random.sample(safety_notes, safety_notes_count)
    inst = random.sample(instructions, instructions_count)

    # generate non-repeating indices in the range [1, len(inst)]
    random_indices = []
    while len(random_indices) < conditionals_count:
        index = random.randrange(1, len(inst), 2)
        if index not in random_indices:
            random_indices.append(index)

    cond = random.sample(conditionals, conditionals_count)

    # insert the conditional senctences into the instructions
    i = 0
    for index in random_indices:
        inst.insert(index, cond[i])
        i += 1

    result += inst
    result += random.sample(finals, finals_count)

    return result


@click.option(
    "--lang",
    "-l",
    type=click.Choice(["de_DE"]),
    default="de_DE",
    help="Set the language of the generated repair instructions.",
)
@click.option(
    "-n",
    default=10,
    help="Number of instructions to be created. Default: 10"
)
@click.option(
    "--quiet",
    is_flag=True,
    default=False,
    help="Do not print the sentences to STDOUT. Default: False",
)
@click.option(
    "--html",
    is_flag=True,
    default=False,
    help="Render HTML output. Default: False"
)
@click.option(
    "--template",
    type=click.Path(),
    default=str(DEFAULT_TEMPLATE),
    help="Specify a custom HTML template to be used.",
)
@click.option(
    "--out",
    type=click.Path(),
    default=f"reapair_{datetime.datetime.now().isoformat()}.html",
    help="Filename of the HTML output file.",
)
@click.option(
    "--overwrite",
    is_flag=True,
    default=False,
    help="Overwrite existing HTML output file. Default: False"
)
@click.command()
def cli(lang, n, quiet, html, template, out, overwrite):
    """
    reapAir is a tool to generate and distribute useful repair instructions for your everyday life.
    """
    try:
        sentences_dict = get_sentences(lang)
    except Exception as e:
        sys.exit(e)

    if n < 1:
        sys.exit(f"Value for '-n' has to be greater than 0. Received: {n}")

    instructions = generate_instructions(sentences_dict, n)

    if not quiet:
        for instruction in instructions:
            print(instruction)

    if html:
        try:
            generateHTML(instructions, template, out, overwrite)
        except Exception as e:
            sys.exit(e)
